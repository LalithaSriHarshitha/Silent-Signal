"""Authentication middleware and dependencies"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.models.user import User
from backend.models.session import Session as UserSession


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_session = db.query(UserSession).filter(
        UserSession.session_token == session_token
    ).first()
    
    if not user_session or user_session.is_expired:
        raise HTTPException(status_code=401, detail="Session expired")
    
    user = db.query(User).filter(User.id == user_session.user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_premium_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to get current premium user"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    return current_user


def get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get user if authenticated, None otherwise"""
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        return None
    
    user_session = db.query(UserSession).filter(
        UserSession.session_token == session_token
    ).first()
    
    if not user_session or user_session.is_expired:
        return None
    
    return db.query(User).filter(User.id == user_session.user_id).first()
