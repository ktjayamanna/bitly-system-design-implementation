from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from redis.exceptions import RedisError

from backend.bitly.db.engine import SessionLocal
from backend.bitly.db.models import Url
from backend.bitly.redis.redis_pool import RedisPool

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def root():
    return {
        "service": "Bitly Read Service",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/ping"
    }

@router.get("/ping")
async def ping(db: Session = Depends(get_db)):
    response = {
        "message": "Read service is up and running!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "read": {"status": "success", "error": None}
        },
        "cache": {
            "status": "success",
            "error": None
        }
    }
    
    try:
        # Test database
        db.query(Url).limit(1).all()
    except SQLAlchemyError as e:
        response["database"]["read"]["status"] = "failed"
        response["database"]["read"]["error"] = str(e)
        raise HTTPException(status_code=500, detail=response)

    try:
        # Test Redis
        redis_client = RedisPool.get_client()
        redis_client.ping()
    except RedisError as e:
        response["cache"]["status"] = "failed"
        response["cache"]["error"] = str(e)
        raise HTTPException(status_code=500, detail=response)
        
    return response
