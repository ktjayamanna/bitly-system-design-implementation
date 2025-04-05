from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from bitly.redis.cache.interface import DataLoaderInterface
from bitly.db.models import Url
from bitly.db.engine import SessionLocal

class UrlDataLoader(DataLoaderInterface):
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load URL data from database"""
        db = SessionLocal()
        try:
            url_entry = db.query(Url).filter(Url.shortened_url == key).first()
            if url_entry:
                return {
                    "original_url": url_entry.original_url,
                    "shortened_url": url_entry.shortened_url,
                    "created_at": url_entry.created_at.isoformat() if url_entry.created_at else None
                }
            return None
        finally:
            db.close()