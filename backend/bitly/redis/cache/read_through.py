import logging
from typing import Any, Optional
from redis.exceptions import RedisError

from bitly.redis.redis_pool import RedisPool
from bitly.redis.helpers.serialization import Serializer
from bitly.redis.constants import URL_CACHE_TTL, REDIS_OPERATION_ERROR
from bitly.redis.cache.interface import CacheInterface, DataLoaderInterface

logger = logging.getLogger(__name__)

class ReadThroughCache(CacheInterface):
    def __init__(self, data_loader: DataLoaderInterface):
        self.redis = RedisPool.get_client()
        self.data_loader = data_loader
        self.serializer = Serializer()

    def get(self, key: str) -> Optional[Any]:
        try:
            # Try to get from cache first
            logger.info(f"Attempting to fetch from Redis cache: {key}")
            cached_value = self.redis.get(key)
            
            if cached_value is not None:
                logger.info(f"Cache HIT for key: {key}")
                return self.serializer.deserialize(cached_value)

            # On cache miss, load from source
            logger.info(f"Cache MISS for key: {key}, loading from database")
            value = self.data_loader.load(key)
            
            if value is not None:
                logger.info(f"Data found in database, caching value for key: {key}")
                self.set(key, value)
                return value
            
            logger.warning(f"Data not found in both cache and database for key: {key}")
            return None

        except RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")

    def set(self, key: str, value: Any, ttl: Optional[int] = URL_CACHE_TTL) -> bool:
        try:
            serialized = self.serializer.serialize(value)
            result = bool(self.redis.setex(key, ttl, serialized) if ttl 
                         else self.redis.set(key, serialized))
            logger.info(f"Cached value for key: {key}, TTL: {ttl}, success: {result}")
            return result
        except RedisError as e:
            logger.error(f"Failed to cache value for key: {key}, error: {str(e)}")
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")

    def delete(self, key: str) -> bool:
        try:
            return bool(self.redis.delete(key))
        except RedisError as e:
            raise Exception(f"{REDIS_OPERATION_ERROR}: {str(e)}")
