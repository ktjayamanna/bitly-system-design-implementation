from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store a value in cache"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Remove a value from cache"""
        pass

class DataLoaderInterface(ABC):
    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """Load data from the primary source"""
        pass