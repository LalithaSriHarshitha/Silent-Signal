"""User model"""
from sqlalchemy import Column, String, Boolean, Integer
from backend.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    workos_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    # Preferences
    preferred_voice_id = Column(String, default="21m00Tcm4TlvDq8ikWAM")
    gesture_sensitivity = Column(String, default="medium")  # low, medium, high
    
    def __repr__(self):
        return f"<User {self.email}>"
