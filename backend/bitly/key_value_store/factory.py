from .store import RedisStore
from .interface import KeyValueStore

class KeyValueStoreFactory:
    _instances: dict[int, KeyValueStore] = {}

    @classmethod
    def get_store(cls, db_index: int = 0) -> KeyValueStore:
        """
        Get a Redis store instance for the specified database index.
        Uses singleton pattern to reuse connections.
        """
        if db_index not in cls._instances:
            cls._instances[db_index] = RedisStore(db_index)
        return cls._instances[db_index]