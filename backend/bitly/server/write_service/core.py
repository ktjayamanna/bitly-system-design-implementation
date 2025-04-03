from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from bitly.db.engine import SessionLocal
from bitly.db.models import User, Url
from .models import UrlCreate, UrlResponse
from bitly.utils.b62 import encode_base62

router = APIRouter()

# Global counter for URL generation
global_counter = 0

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/urls", response_model=UrlResponse)
async def create_short_url(url_data: UrlCreate, db: Session = Depends(get_db)):
    global global_counter
    
    # Verify user exists
    user = db.query(User).filter(User.user_id == url_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Increment counter and generate short URL
        global_counter += 1
        short_code = encode_base62(global_counter).rjust(6, '0')  # Pad to 6 chars
        
        # Create URL entry
        url_entry = Url(
            shortened_url=short_code,
            original_url=str(url_data.original_url),
            owner_id=url_data.user_id,
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(url_entry)
        db.commit()
        db.refresh(url_entry)
        
        return UrlResponse(
            shortened_url=f"http://short.ly/{url_entry.shortened_url}"
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))