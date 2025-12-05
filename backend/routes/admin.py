"""Admin routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.middleware.auth import get_current_user
from backend.models.user import User
from backend.models.gesture import Gesture
from backend.models.subscription import Subscription

router = APIRouter()


@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system statistics (admin only)"""
    # In production, add admin role check
    
    total_users = db.query(func.count(User.id)).scalar()
    total_gestures = db.query(func.count(Gesture.id)).scalar()
    premium_users = db.query(func.count(User.id)).filter(User.is_premium == True).scalar()
    
    return {
        "total_users": total_users,
        "total_gestures": total_gestures,
        "premium_users": premium_users,
        "active_users": total_users,  # Simplified
    }
