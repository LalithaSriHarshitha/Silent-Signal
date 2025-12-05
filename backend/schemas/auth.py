"""Authentication schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class AuthCallbackRequest(BaseModel):
    code: str
    state: Optional[str] = None
