from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError

from bitly.redis.cache.read_through import ReadThroughCache
from bitly.redis.helpers.key_builder import KeyBuilder
from .cache_loader import UrlDataLoader

router = APIRouter()

# Initialize cache with data loader
url_cache = ReadThroughCache(UrlDataLoader())

@router.get("/{short_code}")
async def redirect_to_original_url(short_code: str):
    try:
        # Get cache key
        cache_key = KeyBuilder.build_url_key(short_code)
        
        # Try to get URL from cache
        url_data = url_cache.get(cache_key)
        
        if not url_data:
            raise HTTPException(status_code=404, detail="URL not found")
            
        return RedirectResponse(url=url_data["original_url"], status_code=302)
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
