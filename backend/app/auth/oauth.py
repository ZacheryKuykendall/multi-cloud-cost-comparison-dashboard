from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv
from typing import Optional
import httpx

load_dotenv()

router = APIRouter()
oauth = OAuth()

# AWS Cognito OAuth2 configuration
oauth.register(
    name='aws',
    client_id=os.getenv('AWS_COGNITO_CLIENT_ID'),
    client_secret=os.getenv('AWS_COGNITO_CLIENT_SECRET'),
    server_metadata_url=f"https://{os.getenv('AWS_COGNITO_DOMAIN')}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile'}
)

# Azure AD OAuth2 configuration for organizational access
oauth.register(
    name='azure',
    client_id=os.getenv('AZURE_CLIENT_ID'),
    client_secret=os.getenv('AZURE_CLIENT_SECRET'),
    server_metadata_url=f"https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid email profile https://management.azure.com/user_impersonation'
    }
)

# Google OAuth2 configuration (for GCP)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/cloud-platform'}
)

async def get_azure_token(request: Request) -> Optional[str]:
    """Get Azure access token from session."""
    return request.session.get('azure_token')

async def get_azure_subscriptions(token: str) -> list:
    """Get list of Azure subscriptions user has access to."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://management.azure.com/subscriptions?api-version=2020-01-01',
            headers={'Authorization': f'Bearer {token}'}
        )
        if response.status_code == 200:
            return response.json().get('value', [])
        return []

@router.get("/login/{provider}")
async def login(provider: str, request: Request):
    """Initiate OAuth login flow for specified provider."""
    if provider not in ['aws', 'azure', 'google']:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    redirect_uri = request.url_for('auth_callback', provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)

@router.get("/auth/{provider}/callback")
async def auth_callback(provider: str, request: Request):
    """Handle OAuth callback and token exchange."""
    try:
        token = await oauth.create_client(provider).authorize_access_token(request)
        user = await oauth.create_client(provider).parse_id_token(request, token)
        
        # Store user info in session
        request.session['user'] = {
            'email': user.get('email'),
            'name': user.get('name'),
            'provider': provider
        }

        # For Azure, store additional token and subscription info
        if provider == 'azure':
            access_token = token.get('access_token')
            request.session['azure_token'] = access_token
            subscriptions = await get_azure_subscriptions(access_token)
            request.session['azure_subscriptions'] = subscriptions
        
        # Redirect to frontend with success
        return RedirectResponse(url=f"http://localhost:3000/dashboard?provider={provider}")
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:3000/login?error={str(e)}")

@router.get("/azure/subscriptions")
async def get_user_subscriptions(request: Request):
    """Get Azure subscriptions for the authenticated user."""
    token = await get_azure_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    subscriptions = await get_azure_subscriptions(token)
    return {"subscriptions": subscriptions} 