from typing import List
from redis.exceptions import RedisError
from bitly.redis.redis_pool import RedisPool
from bitly.redis.constants import REDIS_OPERATION_ERROR

class CacheInvalidator:
    def __init__(self):
        self.redis = RedisPool.get_client()

    def invalidate(self, key: str) -> bool:
        """Invalidate a single key"""
        try:
            return bool(self.redis.delete(key))
        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            keys = self.redis.keys(pattern)
            if not keys:
                return 0
            return self.redis.delete(*keys)
        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")
