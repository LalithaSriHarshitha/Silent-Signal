"""Redis cache utilities"""
import redis.asyncio as redis
from typing import Optional, Any
import json
import structlog

from backend.config import settings

logger = structlog.get_logger()


class RedisCache:
    """Redis cache manager"""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        if not settings.REDIS_URL:
            logger.warning("Redis URL not configured, cache disabled")
            return
        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.warning("Failed to connect to Redis, cache disabled", error=str(e))
            self.redis = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            logger.info("Disconnected from Redis")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Redis get error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache"""
        if not self.redis:
            return
        try:
            ttl = ttl or settings.REDIS_CACHE_TTL
            await self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.error("Redis set error", key=key, error=str(e))
    
    async def delete(self, key: str):
        """Delete key from cache"""
        if not self.redis:
            return
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error("Redis delete error", key=key, error=str(e))
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            return False
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error("Redis exists error", key=key, error=str(e))
            return False


# Global cache instance
cache = RedisCache()
