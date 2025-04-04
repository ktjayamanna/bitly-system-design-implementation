from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bitly.db.engine import SessionLocal
from bitly.db.models import Url

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{short_code}")
async def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    try:
        url_entry = db.query(Url).filter(Url.shortened_url == short_code).first()
        if not url_entry:
            raise HTTPException(status_code=404, detail="URL not found")
            
        return RedirectResponse(url=url_entry.original_url, status_code=302)
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))