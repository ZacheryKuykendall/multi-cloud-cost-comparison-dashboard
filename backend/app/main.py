from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import Dict, List, Optional
import asyncio
import os

from app.models import ComputePricing
from app.providers import aws, azure, gcp
from app.cache.redis_cache import RedisCache
from app.auth import oauth_router

app = FastAPI(title="Cloud Marketplace Cost Comparator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key"),  # Change this in production
    max_age=3600  # 1 hour
)

# Initialize Redis cache
cache = RedisCache()

# Include auth routes
app.include_router(oauth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/api/v1/compute/prices", response_model=List[ComputePricing])
async def get_compute_prices(instance_type: str, region: str):
    """
    Get compute prices from all cloud providers for a given instance type and region.
    """
    try:
        # Check cache first
        cached_result = await cache.get(f"compute:{instance_type}:{region}")
        if cached_result:
            return cached_result

        # Fetch prices from all providers concurrently
        tasks = [
            aws.get_compute_prices(instance_type, region),
            azure.get_compute_prices(instance_type, region),
            gcp.get_compute_prices(instance_type, region)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        prices = []
        for result in results:
            if isinstance(result, Exception):
                continue  # Skip failed provider but continue with others
            prices.extend(result)

        # Cache the results
        if prices:
            await cache.set(f"compute:{instance_type}:{region}", prices, expire=3600)  # Cache for 1 hour

        return prices

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/regions")
async def get_regions():
    """
    Get available regions from all cloud providers.
    """
    try:
        # Fetch regions from cache or providers
        cached_regions = await cache.get("regions")
        if cached_regions:
            return cached_regions

        tasks = [
            aws.get_regions(),
            azure.get_regions(),
            gcp.get_regions()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        regions = {}
        for result in results:
            if isinstance(result, Exception):
                continue
            regions.update(result)

        # Cache regions for 24 hours
        await cache.set("regions", regions, expire=86400)
        
        return regions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/instance-types")
async def get_instance_types():
    """
    Get available instance types from all cloud providers.
    """
    try:
        # Fetch instance types from cache or providers
        cached_types = await cache.get("instance_types")
        if cached_types:
            return cached_types

        tasks = [
            aws.get_instance_types(),
            azure.get_instance_types(),
            gcp.get_instance_types()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        instance_types = {}
        for result in results:
            if isinstance(result, Exception):
                continue
            instance_types.update(result)

        # Cache instance types for 24 hours
        await cache.set("instance_types", instance_types, expire=86400)
        
        return instance_types

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 