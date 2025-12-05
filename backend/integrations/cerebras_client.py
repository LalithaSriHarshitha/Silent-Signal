"""Cerebras AI inference client"""
import httpx
from typing import Dict, List, Any
import structlog

from backend.config import settings

logger = structlog.get_logger()


class CerebrasClient:
    """Cerebras AI client for gesture classification"""
    
    def __init__(self):
        self.api_key = settings.CEREBRAS_API_KEY
        self.api_url = settings.CEREBRAS_API_URL
        self.model = settings.CEREBRAS_MODEL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text input"""
        try:
            response = await self.client.post(
                f"{self.api_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "input": text,
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
        except Exception as e:
            logger.error("Embedding generation failed", error=str(e))
            return []
    
    async def classify_intention(
        self,
        gesture_type: str,
        features: List[float],
        context: str = ""
    ) -> Dict[str, Any]:
        """Classify gesture intention using Cerebras"""
        try:
            # Create prompt for intention classification
            prompt = self._build_classification_prompt(gesture_type, features, context)
            
            response = await self.client.post(
                f"{self.api_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an AI that classifies gesture intentions for assistive communication. Respond with JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 150,
                }
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON response
            import json
            classification = json.loads(content)
            
            logger.info("Intention classified", intention=classification.get("intention"))
            return classification
            
        except Exception as e:
            logger.error("Intention classification failed", error=str(e))
            return {
                "intention": "unknown",
                "confidence": 0.0,
                "text": "Unable to process gesture"
            }
    
    def _build_classification_prompt(
        self,
        gesture_type: str,
        features: List[float],
        context: str
    ) -> str:
        """Build prompt for gesture classification"""
        return f"""Classify this gesture into a communication intention:

Gesture Type: {gesture_type}
Features: {features}
Context: {context or "None"}

Common intentions:
- "yes" / "no" / "maybe"
- "help" / "stop" / "continue"
- "hello" / "goodbye"
- "thank_you" / "please"
- "pain" / "discomfort" / "comfortable"
- "hungry" / "thirsty"
- "tired" / "alert"

Respond with JSON:
{{
  "intention": "the_intention",
  "confidence": 0.0-1.0,
  "text": "Natural language text to speak"
}}"""


cerebras_client = CerebrasClient()
