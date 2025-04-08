from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

from bitly.key_value_store.factory import KeyValueStoreFactory
from bitly.key_value_store.interface import KvKeyNotFoundError
from bitly.redis.helpers.key_builder import KeyBuilder
from bitly.server.read_service.cache_loader import UrlDataLoader
from bitly.redis.constants import URL_CACHE_TTL

router = APIRouter()
logger = logging.getLogger(__name__)

# Use db 0 for URL cache
url_store = KeyValueStoreFactory.get_store(db_index=0)

@router.get("/{short_code}")
async def redirect_to_original_url(short_code: str):
    try:
        cache_key = KeyBuilder.build_url_key(short_code)
        try:
            url_data = url_store.get(cache_key)
            return RedirectResponse(url=url_data["original_url"], status_code=302)
        except KvKeyNotFoundError:
            # Load from database and cache
            url_data = UrlDataLoader().load(cache_key)
            if url_data:
                url_store.set(cache_key, url_data, ttl=URL_CACHE_TTL)
                return RedirectResponse(url=url_data["original_url"], status_code=302)
            raise HTTPException(status_code=404, detail="URL not found")
        
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
