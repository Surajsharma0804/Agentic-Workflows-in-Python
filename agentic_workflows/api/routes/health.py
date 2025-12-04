"""Health check endpoints."""
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
import platform
import sys
import os

from ...config import get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str
    timestamp: datetime


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint - Minimal version for Render.com
    
    Returns system health status and basic information.
    """
    try:
        settings = get_settings()
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "timestamp": datetime.utcnow().isoformat(),
            "port": os.getenv("PORT", "unknown")
        }
    except Exception as e:
        # Return minimal response even if settings fail
        return {
            "status": "healthy",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns whether the service is ready to accept requests.
    """
    # Add checks for database, redis, etc.
    return {"status": "ready"}


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check endpoint.
    
    Returns whether the service is alive.
    """
    return {"status": "alive"}
