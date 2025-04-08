from redis import Redis, ConnectionPool, RedisError
from typing import Dict
from bitly.configs import app_configs

class RedisPool:
    _pools: Dict[int, ConnectionPool] = {}

    @classmethod
    def get_pool(cls, db_index: int = 0) -> ConnectionPool:
        if db_index not in cls._pools:
            try:
                cls._pools[db_index] = ConnectionPool(
                    host=app_configs.REDIS_HOST,
                    port=app_configs.REDIS_PORT,
                    db=db_index,
                    decode_responses=True
                )
            except RedisError as e:
                raise ConnectionError(f"Failed to establish Redis connection: {str(e)}")
        return cls._pools[db_index]

    @classmethod
    def get_client(cls, db_index: int = 0) -> Redis:
        return Redis(connection_pool=cls.get_pool(db_index))
