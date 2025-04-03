from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import uuid
import string
from bitly.db.engine import SessionLocal
from bitly.db.models import User, Url
from .models import UrlCreate, UrlResponse

app = FastAPI(title="Write Microservice", version="1.0.0")

# Global counter for URL generation
global_counter = 0

# Base62 characters (0-9, a-z, A-Z)
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num):
    """Convert number to base62 string."""
    if num == 0:
        return BASE62[0]
    
    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "service": "Bitly Write Service",
        "version": app.version,
        "docs_url": "/docs",
        "health_check": "/ping"
    }

@app.get("/ping")
async def ping(db: Session = Depends(get_db)):
    test_username = f"health_check_user_{uuid.uuid4().hex[:8]}"
    test_url = f"test_{uuid.uuid4().hex[:6]}"
    
    response = {
        "message": "Write service is up and running!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "read": {"status": "success", "error": None},
            "write": {"status": "success", "error": None}
        }
    }
    
    # Test write and read
    try:
        # Write test
        test_user = User(user_name=test_username)
        db.add(test_user)
        db.flush()
        test_url_entry = Url(
            shortened_url=test_url,
            original_url="https://health.check.test",
            owner_id=test_user.user_id
        )
        db.add(test_url_entry)
        db.commit()
        
        # Read test
        db.query(User).filter(User.user_name == test_username).first()
        db.query(Url).filter(Url.shortened_url == test_url).first()
        
        # Cleanup
        db.query(Url).filter(Url.shortened_url == test_url).delete()
        db.query(User).filter(User.user_name == test_username).delete()
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        response["database"]["write"]["status"] = "failed"
        response["database"]["write"]["error"] = str(e)
        raise HTTPException(status_code=500, detail=response)
        
    return response

@app.post("/urls", response_model=UrlResponse)
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
