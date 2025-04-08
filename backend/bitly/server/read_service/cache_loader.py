import logging
from typing import Optional, Dict, Any
from bitly.key_value_store.interface import DataLoaderInterface
from bitly.db.models import Url
from bitly.db.engine import SessionLocal

logger = logging.getLogger(__name__)

class UrlDataLoader(DataLoaderInterface):
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load URL data from database"""
        # Extract short_code from Redis key (remove 'url:' prefix)
        short_code = key.split(':')[-1]
        logger.info(f"Loading from database for short_code: {short_code}")
        
        db = SessionLocal()
        try:
            url_entry = db.query(Url).filter(Url.shortened_url == short_code).first()
            if url_entry:
                logger.info(f"Found URL in database: {url_entry.original_url}")
                return {
                    "original_url": url_entry.original_url,
                    "shortened_url": url_entry.shortened_url,
                    "created_at": url_entry.created_at.isoformat() if url_entry.created_at else None
                }
            logger.warning(f"URL not found in database for short_code: {short_code}")
            return None
        finally:
            db.close()
