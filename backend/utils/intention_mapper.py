"""Map classified intentions to text output"""
from typing import Dict, Optional
import structlog

logger = structlog.get_logger()


class IntentionMapper:
    """Map intentions to natural language text"""
    
    # Predefined intention mappings
    INTENTION_MAP = {
        "yes": "Yes",
        "no": "No",
        "maybe": "Maybe",
        "help": "I need help",
        "stop": "Please stop",
        "continue": "Please continue",
        "hello": "Hello",
        "goodbye": "Goodbye",
        "thank_you": "Thank you",
        "please": "Please",
        "pain": "I'm in pain",
        "discomfort": "I'm uncomfortable",
        "comfortable": "I'm comfortable",
        "hungry": "I'm hungry",
        "thirsty": "I'm thirsty",
        "tired": "I'm tired",
        "alert": "I'm alert",
        "bathroom": "I need to use the bathroom",
        "water": "I need water",
        "medicine": "I need my medicine",
        "call_nurse": "Please call the nurse",
        "call_doctor": "Please call the doctor",
        "family": "I want to see my family",
        "rest": "I need to rest",
        "sit_up": "Help me sit up",
        "lie_down": "Help me lie down",
        "cold": "I'm cold",
        "hot": "I'm hot",
        "music": "I want to listen to music",
        "tv": "I want to watch TV",
        "read": "I want to read",
        "talk": "I want to talk",
        "alone": "I want to be alone",
        "unknown": "I'm trying to communicate something",
    }
    
    @staticmethod
    def map_intention_to_text(intention: str, custom_text: Optional[str] = None) -> str:
        """Map intention to natural language text"""
        if custom_text:
            return custom_text
        
        text = IntentionMapper.INTENTION_MAP.get(intention.lower(), "I'm trying to communicate")
        logger.debug("Intention mapped", intention=intention, text=text)
        return text
    
    @staticmethod
    def get_all_intentions() -> Dict[str, str]:
        """Get all available intentions"""
        return IntentionMapper.INTENTION_MAP.copy()
    
    @staticmethod
    def add_custom_intention(intention: str, text: str):
        """Add custom intention mapping"""
        IntentionMapper.INTENTION_MAP[intention.lower()] = text
        logger.info("Custom intention added", intention=intention)


intention_mapper = IntentionMapper()
