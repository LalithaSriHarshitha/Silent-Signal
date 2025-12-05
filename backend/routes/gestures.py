"""Gesture processing routes"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import time
import structlog

from backend.database import get_db
from backend.middleware.auth import get_current_user
from backend.models.user import User
from backend.models.gesture import Gesture
from backend.schemas.gesture import GestureCreate, GestureResponse
from backend.services.gesture_service import gesture_service

logger = structlog.get_logger()
router = APIRouter()


@router.websocket("/ws")
async def gesture_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time gesture streaming"""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive gesture data
            data = await websocket.receive_text()
            gesture_data = json.loads(data)
            
            start_time = time.time()
            
            # Process gesture through pipeline
            result = await gesture_service.process_gesture_stream(
                db=db,
                user_id=gesture_data.get("user_id"),
                gesture_type=gesture_data.get("gesture_type"),
                raw_data=gesture_data.get("data")
            )
            
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = processing_time
            
            # Send response back
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
        await websocket.close(code=1011, reason=str(e))


@router.post("/", response_model=GestureResponse)
async def create_gesture(
    gesture: GestureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """HTTP endpoint for gesture submission (fallback)"""
    start_time = time.time()
    
    result = await gesture_service.process_gesture(
        db=db,
        user_id=current_user.id,
        gesture_type=gesture.gesture_type,
        raw_data=gesture.raw_data
    )
    
    processing_time = (time.time() - start_time) * 1000
    result.processing_time_ms = processing_time
    
    return result


@router.get("/", response_model=List[GestureResponse])
async def get_user_gestures(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's gesture history"""
    gestures = db.query(Gesture).filter(
        Gesture.user_id == current_user.id
    ).order_by(Gesture.created_at.desc()).offset(skip).limit(limit).all()
    
    return gestures


@router.get("/{gesture_id}", response_model=GestureResponse)
async def get_gesture(
    gesture_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific gesture by ID"""
    gesture = db.query(Gesture).filter(
        Gesture.id == gesture_id,
        Gesture.user_id == current_user.id
    ).first()
    
    if not gesture:
        raise HTTPException(status_code=404, detail="Gesture not found")
    
    return gesture


@router.delete("/{gesture_id}")
async def delete_gesture(
    gesture_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a gesture"""
    gesture = db.query(Gesture).filter(
        Gesture.id == gesture_id,
        Gesture.user_id == current_user.id
    ).first()
    
    if not gesture:
        raise HTTPException(status_code=404, detail="Gesture not found")
    
    db.delete(gesture)
    db.commit()
    
    return {"message": "Gesture deleted successfully"}
