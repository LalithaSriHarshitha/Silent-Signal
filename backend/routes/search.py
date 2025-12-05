"""Search and analytics routes"""
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any

from backend.middleware.auth import get_current_user
from backend.models.user import User
from backend.integrations.searchable_client import searchable_client

router = APIRouter()


@router.get("/gestures")
async def search_gestures(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Search user's gestures"""
    results = await searchable_client.search_gestures(
        query=q,
        user_id=current_user.id,
        limit=limit
    )
    return results


@router.get("/analytics")
async def get_analytics(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get user analytics"""
    analytics = await searchable_client.get_analytics(current_user.id)
    return analytics
