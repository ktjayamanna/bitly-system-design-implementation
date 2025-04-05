from redis import Redis, ConnectionPool, RedisError
from typing import Optional
import os
from bitly.redis.constants import REDIS_CONNECTION_ERROR

from dotenv import load_dotenv
load_dotenv(".vscode/.env")

class RedisPool:
    _instance: Optional[ConnectionPool] = None

    @classmethod
    def get_pool(cls) -> ConnectionPool:
        if cls._instance is None:
            try:
                cls._instance = ConnectionPool(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", 6379)),
                    db=int(os.getenv("REDIS_DB", 0)),
                    decode_responses=True
                )
            except RedisError as e:
                raise ConnectionError(f"{REDIS_CONNECTION_ERROR}: {str(e)}")
        return cls._instance

    @classmethod
    def get_client(cls) -> Redis:
        return Redis(connection_pool=cls.get_pool())
