from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from bitly.db.engine import SessionLocal
from bitly.db.models import Url

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
        }
    }
    
    try:
        # Simple read test
        db.query(Url).limit(1).all()
        
    except SQLAlchemyError as e:
        response["database"]["read"]["status"] = "failed"
        response["database"]["read"]["error"] = str(e)
        raise HTTPException(status_code=500, detail=response)
        
    return response