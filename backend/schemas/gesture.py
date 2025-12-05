"""Gesture schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class GestureCreate(BaseModel):
    gesture_type: str  # blink, tap, micro_gesture
    raw_data: Optional[Dict[str, Any]] = None


class GestureResponse(BaseModel):
    id: int
    user_id: int
    gesture_type: str
    intention: Optional[str] = None
    confidence_score: Optional[float] = None
    generated_text: Optional[str] = None
    audio_url: Optional[str] = None
    processing_time_ms: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GestureStreamData(BaseModel):
    """Real-time gesture stream data"""
    gesture_type: str
    timestamp: float
    data: Dict[str, Any]


class IntentionResponse(BaseModel):
    """AI intention classification response"""
    intention: str
    confidence: float
    text: str
    audio_url: Optional[str] = None
