# Cloud Marketplace Cost Comparator

A modern web application that compares compute pricing across AWS, Azure, and GCP cloud providers. Built with FastAPI, React, and Docker, featuring OAuth2 authentication for each cloud provider.

## Features

- **Multi-Cloud Authentication**
  - AWS Cognito integration
  - Azure AD organizational authentication
  - Google Cloud OAuth2 support
  - Secure session management

- **Real-time Price Comparison**
  - Compute instance pricing across all three major cloud providers
  - Support for multiple pricing models:
    - On-demand pricing
    - Spot/Preemptible instances
    - Reserved instances (1-year and 3-year terms)
  - Region-specific pricing
  - Instance type mapping across providers

- **Modern UI/UX**
  - Interactive charts using Recharts
  - Material-UI components
  - Dark/Light mode support
  - Responsive design for all screen sizes
  - Real-time price updates
  - Subscription management for Azure

- **Performance Features**
  - Redis caching for improved response times
  - Asynchronous API calls
  - Docker containerization
  - Nginx reverse proxy

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Cloud Provider Credentials:
  - AWS Cognito User Pool
  - Azure AD Application
  - Google Cloud OAuth2 Client

## Environment Setup

1. Create a `.env` file in the root directory with the following configurations:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_COGNITO_CLIENT_ID=your_cognito_client_id
AWS_COGNITO_CLIENT_SECRET=your_cognito_client_secret
AWS_COGNITO_DOMAIN=your_cognito_domain

# Azure Configuration
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AZURE_TENANT_ID=your_azure_tenant_id

# Google Cloud Configuration
GCP_PROJECT_ID=your_gcp_project_id
GCP_API_KEY=your_gcp_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Application Security
SECRET_KEY=your_secret_key_for_session_encryption

# Redis Configuration (optional)
REDIS_URL=redis://redis:6379
```

## OAuth2 Setup Guide

### AWS Cognito Setup
1. Go to AWS Console > Cognito
2. Create a new User Pool
3. Add an app client with OAuth2 enabled
4. Configure callback URL: `http://localhost:3000/api/v1/auth/aws/callback`
5. Enable authorization code grant flow
6. Copy credentials to `.env` file

### Azure AD Setup
1. Go to Azure Portal > Azure Active Directory
2. Register a new application
3. Add redirect URI: `http://localhost:3000/api/v1/auth/azure/callback`
4. Create a client secret
5. Grant admin consent for:
   - `openid`
   - `email`
   - `profile`
   - `https://management.azure.com/user_impersonation`
6. Copy credentials to `.env` file

### Google Cloud Setup
1. Go to Google Cloud Console > APIs & Services
2. Create OAuth2 credentials
3. Add authorized redirect URI: `http://localhost:3000/api/v1/auth/google/callback`
4. Enable Cloud Billing API
5. Copy credentials to `.env` file

## Installation & Running

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ZacheryKuykendall/multi-cloud-cost-comparison-dashboard.git
cd multi-cloud-cost-comparison-dashboard

# Create and configure .env file
cp .env.example .env
# Edit .env with your credentials

# Build and run with Docker Compose
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication Endpoints
- `GET /api/v1/auth/login/{provider}` - Initiate OAuth2 login
- `GET /api/v1/auth/{provider}/callback` - OAuth2 callback handler
- `GET /api/v1/auth/azure/subscriptions` - Get Azure subscriptions

### Pricing Endpoints
- `GET /api/v1/compute/prices` - Get compute prices across providers
- `GET /api/v1/regions` - List available regions
- `GET /api/v1/instance-types` - List available instance types

## Architecture

### Backend
- FastAPI for high-performance async API
- Redis caching layer
- Provider-specific modules for AWS, Azure, and GCP
- Session-based authentication
- Pydantic models for validation

### Frontend
- React with TypeScript
- Material-UI components
- Recharts for visualizations
- Axios for API communication
- Responsive layout system

### Infrastructure
- Docker containers for all services
- Nginx reverse proxy
- Redis for caching
- Docker Compose orchestration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository. 