"""Subscription model"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from backend.models.base import Base, TimestampMixin


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    stripe_price_id = Column(String, nullable=True)
    
    tier = Column(String, default="free")  # free, premium
    status = Column(String, default="active")  # active, canceled, past_due
    
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Subscription user_id={self.user_id} tier={self.tier}>"
