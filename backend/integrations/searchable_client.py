"""Searchable search and analytics client"""
import httpx
from typing import Dict, List, Any
import structlog

from backend.config import settings

logger = structlog.get_logger()


class SearchableClient:
    """Searchable indexing and search client"""
    
    def __init__(self):
        self.api_key = settings.SEARCHABLE_API_KEY
        self.api_url = settings.SEARCHABLE_API_URL
        self.index_name = settings.SEARCHABLE_INDEX_NAME
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def index_gesture(self, gesture) -> bool:
        """Index gesture for search"""
        try:
            document = {
                "id": str(gesture.id),
                "user_id": gesture.user_id,
                "gesture_type": gesture.gesture_type,
                "intention": gesture.intention,
                "text": gesture.generated_text,
                "confidence": gesture.confidence_score,
                "timestamp": gesture.created_at.isoformat(),
            }
            
            response = await self.client.post(
                f"{self.api_url}/indexes/{self.index_name}/documents",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=document
            )
            response.raise_for_status()
            logger.debug("Gesture indexed", gesture_id=gesture.id)
            return True
        except Exception as e:
            logger.error("Indexing failed", error=str(e))
            return False

    
    async def search_gestures(
        self,
        query: str,
        user_id: int = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search gestures"""
        try:
            filters = {}
            if user_id:
                filters["user_id"] = user_id
            
            response = await self.client.post(
                f"{self.api_url}/indexes/{self.index_name}/search",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "query": query,
                    "filters": filters,
                    "limit": limit,
                }
            )
            response.raise_for_status()
            results = response.json()
            return results.get("hits", [])
        except Exception as e:
            logger.error("Search failed", error=str(e))
            return []
    
    async def get_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get gesture analytics for user"""
        try:
            response = await self.client.get(
                f"{self.api_url}/indexes/{self.index_name}/analytics",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"user_id": user_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Analytics retrieval failed", error=str(e))
            return {}


searchable_client = SearchableClient()
