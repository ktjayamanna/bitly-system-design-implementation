from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

from bitly.redis.cache.read_through import ReadThroughCache
from bitly.redis.helpers.key_builder import KeyBuilder
from .cache_loader import UrlDataLoader

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize cache with data loader
url_cache = ReadThroughCache(UrlDataLoader())

@router.get("/{short_code}")
async def redirect_to_original_url(short_code: str):
    try:
        # Get cache key
        cache_key = KeyBuilder.build_url_key(short_code)
        logger.info(f"Processing request for short_code: {short_code}, cache_key: {cache_key}")
        
        # Try to get URL from cache (this will also try database if cache misses)
        url_data = url_cache.get(cache_key)
        
        if not url_data:
            logger.warning(f"URL not found for short_code: {short_code}")
            raise HTTPException(status_code=404, detail="URL not found")
            
        logger.info(f"Found URL data: {url_data}")
        return RedirectResponse(url=url_data["original_url"], status_code=302)
        
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
