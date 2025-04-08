import logging
from typing import Any, Optional
from redis.exceptions import RedisError

from bitly.redis.redis_pool import RedisPool
from bitly.redis.helpers.serialization import Serializer
from .interface import KeyValueStore, KvKeyNotFoundError

logger = logging.getLogger(__name__)

class RedisStore(KeyValueStore):
    def __init__(self, db_index: int = 0):
        self.redis = RedisPool.get_client(db_index)
        self.serializer = Serializer()

    def get(self, key: str) -> Any:
        try:
            value = self.redis.get(key)
            if value is None:
                raise KvKeyNotFoundError(f"Key not found: {key}")
            return self.serializer.deserialize(value)
        except RedisError as e:
            logger.error(f"Redis error in get: {str(e)}")
            raise

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            serialized = self.serializer.serialize(value)
            return bool(
                self.redis.setex(key, ttl, serialized) if ttl 
                else self.redis.set(key, serialized)
            )
        except RedisError as e:
            logger.error(f"Redis error in set: {str(e)}")
            raise

    def delete(self, key: str) -> bool:
        try:
            return bool(self.redis.delete(key))
        except RedisError as e:
            logger.error(f"Redis error in delete: {str(e)}")
            raise

    def increment(self, key: str, amount: int = 1) -> int:
        try:
            return self.redis.incrby(key, amount)
        except RedisError as e:
            logger.error(f"Redis error in increment: {str(e)}")
            raise