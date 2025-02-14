import json
import redis.asyncio as redis
from typing import Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    def __init__(self):
        """Initialize Redis connection."""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        """
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {str(e)}")
            return None

    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        Set value in cache with expiration time in seconds.
        """
        try:
            await self.redis.setex(
                key,
                expire,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        """
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {str(e)}")
            return False

    async def clear(self) -> bool:
        """
        Clear all cache.
        """
        try:
            await self.redis.flushdb()
            return True
        except Exception as e:
            print(f"Redis clear error: {str(e)}")
            return False 