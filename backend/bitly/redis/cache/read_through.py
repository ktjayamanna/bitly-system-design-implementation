from typing import Any, Optional
from redis.exceptions import RedisError

from bitly.redis.redis_pool import RedisPool
from bitly.redis.helpers.serialization import Serializer
from bitly.redis.constants import URL_CACHE_TTL, REDIS_OPERATION_ERROR
from bitly.redis.cache.interface import CacheInterface, DataLoaderInterface

class ReadThroughCache(CacheInterface):
    def __init__(self, data_loader: DataLoaderInterface):
        self.redis = RedisPool.get_client()
        self.data_loader = data_loader
        self.serializer = Serializer()

    def get(self, key: str) -> Optional[Any]:
        try:
            # Try to get from cache first
            cached_value = self.redis.get(key)
            if cached_value is not None:
                return self.serializer.deserialize(cached_value)

            # On cache miss, load from source
            value = self.data_loader.load(key)
            if value is not None:
                self.set(key, value)
            return value

        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")

    def set(self, key: str, value: Any, ttl: Optional[int] = URL_CACHE_TTL) -> bool:
        try:
            serialized = self.serializer.serialize(value)
            return bool(self.redis.setex(key, ttl, serialized) if ttl 
                       else self.redis.set(key, serialized))
        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")

    def delete(self, key: str) -> bool:
        try:
            return bool(self.redis.delete(key))
        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")