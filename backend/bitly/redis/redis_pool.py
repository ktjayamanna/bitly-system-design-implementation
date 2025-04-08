from redis import Redis, ConnectionPool, RedisError
from typing import Dict
import os

from dotenv import load_dotenv
load_dotenv(".vscode/.env")

class RedisPool:
    _pools: Dict[int, ConnectionPool] = {}

    @classmethod
    def get_pool(cls, db_index: int = 0) -> ConnectionPool:
        if db_index not in cls._pools:
            try:
                cls._pools[db_index] = ConnectionPool(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", 6379)),
                    db=db_index,
                    decode_responses=True
                )
            except RedisError as e:
                raise ConnectionError(f"Failed to establish Redis connection: {str(e)}")
        return cls._pools[db_index]

    @classmethod
    def get_client(cls, db_index: int = 0) -> Redis:
        return Redis(connection_pool=cls.get_pool(db_index))
