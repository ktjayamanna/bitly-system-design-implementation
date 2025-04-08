from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

class KvKeyNotFoundError(Exception):
    """Raised when a key is not found in the store"""
    pass

class KeyValueStore(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieve a value from store"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store a value"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Remove a value"""
        pass

    @abstractmethod
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter"""
        pass

class DataLoaderInterface(ABC):
    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load data from the data source"""
        pass
