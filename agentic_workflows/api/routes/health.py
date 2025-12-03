"""Health check endpoints."""
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
import platform
import sys

from ...config import get_settings

router = APIRouter()
settings = get_settings()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str
    timestamp: datetime
    system_info: dict


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    
    Returns system health status and basic information.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
        timestamp=datetime.utcnow(),
        system_info={
            "python_version": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
        }
    )


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
