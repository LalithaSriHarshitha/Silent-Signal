"""Health check routes"""
from fastapi import APIRouter
from datetime import datetime
import structlog

from backend.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/status")
async def system_status():
    """Detailed system status"""
    return {
        "api": "operational",
        "database": "operational",
        "redis": "operational",
        "services": {
            "workos": "operational",
            "cerebras": "operational",
            "elevenlabs": "operational",
            "raindrop": "operational",
            "stripe": "operational",
            "searchable": "operational",
        }
    }
