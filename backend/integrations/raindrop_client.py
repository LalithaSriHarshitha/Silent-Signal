"""LiquidMetal AI Raindrop client"""
import httpx
from typing import Dict, Any
import structlog

from backend.config import settings

logger = structlog.get_logger()


class RaindropClient:
    """Raindrop SmartFlow orchestration client"""
    
    def __init__(self):
        self.api_key = settings.RAINDROP_API_KEY
        self.api_url = settings.RAINDROP_API_URL
        self.smartflow_id = settings.RAINDROP_SMARTFLOW_ID
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def execute_smartflow(
        self,
        flow_name: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a Raindrop SmartFlow"""
        try:
            response = await self.client.post(
                f"{self.api_url}/smartflows/{self.smartflow_id}/execute",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "flow_name": flow_name,
                    "input": input_data,
                }
            )
            response.raise_for_status()
            result = response.json()
            logger.info("SmartFlow executed", flow_name=flow_name)
            return result
        except Exception as e:
            logger.error("SmartFlow execution failed", error=str(e))
            return {"error": str(e)}

    
    async def route_gesture_pipeline(
        self,
        gesture_type: str,
        features: list,
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route gesture through ML pipeline"""
        return await self.execute_smartflow(
            flow_name="gesture_classification",
            input_data={
                "gesture_type": gesture_type,
                "features": features,
                "user_context": user_context,
            }
        )
    
    async def get_secret(self, secret_name: str) -> str:
        """Retrieve secret from Raindrop"""
        try:
            response = await self.client.get(
                f"{self.api_url}/secrets/{secret_name}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json().get("value", "")
        except Exception as e:
            logger.error("Secret retrieval failed", secret=secret_name, error=str(e))
            return ""
    
    async def store_secret(self, secret_name: str, secret_value: str) -> bool:
        """Store secret in Raindrop"""
        try:
            response = await self.client.post(
                f"{self.api_url}/secrets",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={"name": secret_name, "value": secret_value}
            )
            response.raise_for_status()
            logger.info("Secret stored", secret=secret_name)
            return True
        except Exception as e:
            logger.error("Secret storage failed", error=str(e))
            return False


raindrop_client = RaindropClient()
