from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base
from datetime import datetime

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    url_code = Column(String, index=True)
    user_agent = Column(String)
    ip_address = Column(String)
    location = Column(String, nullable=True)
    
    latitude = Column(Float, nullable=True)  # Latitude field
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
