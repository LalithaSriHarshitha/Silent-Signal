"""Gesture processing service"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import structlog

from backend.models.gesture import Gesture
from backend.utils.gesture_preprocessor import gesture_preprocessor
from backend.integrations.cerebras_client import cerebras_client
from backend.utils.intention_mapper import intention_mapper
from backend.integrations.elevenlabs_client import elevenlabs_client
from backend.integrations.raindrop_client import raindrop_client
from backend.integrations.searchable_client import searchable_client

logger = structlog.get_logger()


class GestureService:
    """Service for processing gestures through the full pipeline"""
    
    async def process_gesture(
        self,
        db: Session,
        user_id: int,
        gesture_type: str,
        raw_data: Optional[Dict[str, Any]] = None
    ) -> Gesture:
        """Process gesture through full pipeline"""
        # Validate and normalize
        if not gesture_preprocessor.validate_gesture_data(gesture_type, raw_data or {}):
            logger.warning("Invalid gesture data", gesture_type=gesture_type)
        
        # Normalize based on type
        normalized_data = self._normalize_gesture(gesture_type, raw_data or {})
        
        # Extract features
        features = gesture_preprocessor.extract_features(gesture_type, normalized_data)

        
        # Classify intention via Cerebras
        classification = await cerebras_client.classify_intention(
            gesture_type=gesture_type,
            features=features,
            context=""
        )
        
        intention = classification.get("intention", "unknown")
        confidence = classification.get("confidence", 0.0)
        
        # Map to text
        text = intention_mapper.map_intention_to_text(
            intention,
            classification.get("text")
        )
        
        # Generate speech via ElevenLabs
        audio_url = await elevenlabs_client.text_to_speech(text, user_id)
        
        # Create gesture record
        gesture = Gesture(
            user_id=user_id,
            gesture_type=gesture_type,
            raw_data=raw_data,
            embedding=features,
            intention=intention,
            confidence_score=confidence,
            generated_text=text,
            audio_url=audio_url,
        )
        
        db.add(gesture)
        db.commit()
        db.refresh(gesture)
        
        # Index in Searchable
        await searchable_client.index_gesture(gesture)
        
        logger.info("Gesture processed", gesture_id=gesture.id, intention=intention)
        return gesture
    
    async def process_gesture_stream(
        self,
        db: Session,
        user_id: int,
        gesture_type: str,
        raw_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process gesture for WebSocket streaming"""
        gesture = await self.process_gesture(db, user_id, gesture_type, raw_data)
        
        return {
            "gesture_id": gesture.id,
            "intention": gesture.intention,
            "confidence": gesture.confidence_score,
            "text": gesture.generated_text,
            "audio_url": gesture.audio_url,
        }
    
    def _normalize_gesture(self, gesture_type: str, raw_data: Dict) -> Dict:
        """Normalize gesture data based on type"""
        if gesture_type == "blink":
            return gesture_preprocessor.normalize_blink_data(raw_data)
        elif gesture_type == "tap":
            return gesture_preprocessor.normalize_tap_data(raw_data)
        elif gesture_type == "micro_gesture":
            return gesture_preprocessor.normalize_micro_gesture_data(raw_data)
        return raw_data


gesture_service = GestureService()
