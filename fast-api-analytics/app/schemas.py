from pydantic import BaseModel
from datetime import datetime

class ClickCreate(BaseModel):
    url_code: str
    user_agent: str
    ip_address: str
    location: str = None

class ClickOut(BaseModel):
    url_code: str
    created_at: datetime
    user_agent: str
    ip_address: str
    location: str
