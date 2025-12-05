"""Gesture data preprocessing utilities"""
from typing import Dict, Any, List
import numpy as np
import structlog

logger = structlog.get_logger()


class GesturePreprocessor:
    """Preprocess and normalize gesture data"""
    
    @staticmethod
    def normalize_blink_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize blink detection data"""
        try:
            return {
                "duration_ms": raw_data.get("duration", 0),
                "intensity": raw_data.get("intensity", 0.5),
                "eye": raw_data.get("eye", "both"),  # left, right, both
                "timestamp": raw_data.get("timestamp", 0),
            }
        except Exception as e:
            logger.error("Blink normalization failed", error=str(e))
            return {}
    
    @staticmethod
    def normalize_tap_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize tap gesture data"""
        try:
            return {
                "tap_count": raw_data.get("count", 1),
                "interval_ms": raw_data.get("interval", 0),
                "pressure": raw_data.get("pressure", 0.5),
                "location": raw_data.get("location", "unknown"),
                "timestamp": raw_data.get("timestamp", 0),
            }
        except Exception as e:
            logger.error("Tap normalization failed", error=str(e))
            return {}
    
    @staticmethod
    def normalize_micro_gesture_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize micro-gesture data"""
        try:
            return {
                "gesture_name": raw_data.get("name", "unknown"),
                "confidence": raw_data.get("confidence", 0.0),
                "keypoints": raw_data.get("keypoints", []),
                "timestamp": raw_data.get("timestamp", 0),
            }
        except Exception as e:
            logger.error("Micro-gesture normalization failed", error=str(e))
            return {}
    
    @staticmethod
    def validate_gesture_data(gesture_type: str, raw_data: Dict[str, Any]) -> bool:
        """Validate gesture data structure"""
        if not raw_data:
            return False
        
        required_fields = {
            "blink": ["duration", "timestamp"],
            "tap": ["count", "timestamp"],
            "micro_gesture": ["name", "confidence", "timestamp"],
        }
        
        fields = required_fields.get(gesture_type, [])
        return all(field in raw_data for field in fields)
    
    @staticmethod
    def extract_features(gesture_type: str, normalized_data: Dict[str, Any]) -> List[float]:
        """Extract numerical features for ML processing"""
        features = []
        
        if gesture_type == "blink":
            features = [
                normalized_data.get("duration_ms", 0) / 1000.0,
                normalized_data.get("intensity", 0.5),
                1.0 if normalized_data.get("eye") == "both" else 0.5,
            ]
        elif gesture_type == "tap":
            features = [
                normalized_data.get("tap_count", 1),
                normalized_data.get("interval_ms", 0) / 1000.0,
                normalized_data.get("pressure", 0.5),
            ]
        elif gesture_type == "micro_gesture":
            features = [
                normalized_data.get("confidence", 0.0),
                len(normalized_data.get("keypoints", [])),
            ]
        
        return features


gesture_preprocessor = GesturePreprocessor()
