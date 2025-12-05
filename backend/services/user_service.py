"""User service for business logic"""
from sqlalchemy.orm import Session
from typing import Optional
import structlog

from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()


class UserService:
    """User management service"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_workos_id(db: Session, workos_id: str) -> Optional[User]:
        """Get user by WorkOS ID"""
        return db.query(User).filter(User.workos_id == workos_id).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create new user"""
        user = User(
            workos_id=user_data.workos_id,
            email=user_data.email,
            full_name=user_data.full_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("User created", user_id=user.id, email=user.email)
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        logger.info("User updated", user_id=user.id)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user (soft delete by setting is_active=False)"""
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        user.is_active = False
        db.commit()
        logger.info("User deactivated", user_id=user.id)
        return True


user_service = UserService()
