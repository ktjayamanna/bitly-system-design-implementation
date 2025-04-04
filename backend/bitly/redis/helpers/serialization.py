import json
from typing import Any, Optional

class Serializer:
    @staticmethod
    def serialize(value: Any) -> str:
        """Serialize value to string"""
        return json.dumps(value)

    @staticmethod
    def deserialize(value: Optional[str]) -> Any:
        """Deserialize string to value"""
        return json.loads(value) if value else None