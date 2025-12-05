"""User schemas"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    workos_id: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_voice_id: Optional[str] = None
    gesture_sensitivity: Optional[str] = None


class UserResponse(UserBase):
    id: int
    workos_id: str
    is_active: bool
    is_premium: bool
    preferred_voice_id: str
    gesture_sensitivity: str
    created_at: datetime
    
    class Config:
        from_attributes = True
