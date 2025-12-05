"""User management routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.middleware.auth import get_current_user
from backend.models.user import User
from backend.schemas.user import UserResponse, UserUpdate
from backend.services.user_service import user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    updated_user = user_service.update_user(db, current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user


@router.get("/preferences")
async def get_user_preferences(
    current_user: User = Depends(get_current_user)
):
    """Get user preferences"""
    return {
        "preferred_voice_id": current_user.preferred_voice_id,
        "gesture_sensitivity": current_user.gesture_sensitivity,
    }


@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    if "preferred_voice_id" in preferences:
        current_user.preferred_voice_id = preferences["preferred_voice_id"]
    if "gesture_sensitivity" in preferences:
        current_user.gesture_sensitivity = preferences["gesture_sensitivity"]
    
    db.commit()
    return {"message": "Preferences updated successfully"}
