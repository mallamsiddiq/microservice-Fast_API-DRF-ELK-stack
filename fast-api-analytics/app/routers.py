from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio
from sqlalchemy import func
from . import models, schemas
from .database import get_db
from .utils import get_location_from_ip
from .analytics import send_event_click_event

router = APIRouter()

@router.post("/track-click/", response_model=schemas.ClickOut)
def track_click(click_data: schemas.ClickCreate, db: Session = Depends(get_db)):
    location_data = get_location_from_ip(click_data.ip_address)
    
    click_data = {
        "url_code":click_data.url_code,
        "user_agent":click_data.user_agent,
        "ip_address":click_data.ip_address,
        "location":f"{location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}",
        "latitude":location_data.get("latitude"),
        "longitude":location_data.get("longitude"),
    }

    click = models.Click(**click_data)
    send_event_click_event(click_data)
    # Asynchronously send the click event to Kafka
    # asyncio.create_task(send_event_click_event(click_data))
    db.add(click)
    db.commit()
    db.refresh(click)
    return click



@router.get("/analytics-report/")
def analytics_report(db: Session = Depends(get_db)):
    report = db.query(models.Click.url_code, func.count(models.Click.id)\
                      .label("click_count")).group_by(models.Click.url_code).all()
    return {"report": report}


