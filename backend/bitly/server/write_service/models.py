
from pydantic import BaseModel, HttpUrl

class UrlCreate(BaseModel):
    original_url: HttpUrl
    user_id: int

class UrlResponse(BaseModel):
    shortened_url: str

