"""Redis client."""
import redis
import json
from typing import Any, Optional
from ..config import get_settings

settings = get_settings()

class RedisClient:
    """Redis client wrapper."""
    
    def __init__(self):
        self.client = redis.from_url(
            settings.redis_url,
            max_connections=settings.redis_max_connections,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache."""
        self.client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        """Delete key from cache."""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return self.client.exists(key) > 0

redis_client = RedisClient()
