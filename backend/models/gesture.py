"""Gesture model"""
from sqlalchemy import Column, String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base, TimestampMixin


class Gesture(Base, TimestampMixin):
    __tablename__ = "gestures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Gesture data
    gesture_type = Column(String, nullable=False)  # blink, tap, micro_gesture
    raw_data = Column(JSON, nullable=True)  # Raw sensor/camera data
    
    # AI Processing
    embedding = Column(JSON, nullable=True)  # Cerebras embedding
    intention = Column(String, nullable=True)  # Classified intention
    confidence_score = Column(Float, nullable=True)
    
    # Output
    generated_text = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)  # ElevenLabs audio URL
    
    # Metadata
    processing_time_ms = Column(Float, nullable=True)
    raindrop_flow_id = Column(String, nullable=True)
    
    user = relationship("User", backref="gestures")
    
    def __repr__(self):
        return f"<Gesture {self.gesture_type} - {self.intention}>"
