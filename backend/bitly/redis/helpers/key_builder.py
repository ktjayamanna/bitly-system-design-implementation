from backend.bitly.redis.constants import URL_CACHE_PREFIX

class KeyBuilder:
    @staticmethod
    def build_url_key(short_code: str) -> str:
        """Builds a Redis key for URL caching (e.g., url:abc123)"""
        return f"{URL_CACHE_PREFIX}:{short_code}"
