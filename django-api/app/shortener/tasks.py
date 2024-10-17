# tasks.py
from celery import shared_task
import requests

@shared_task
def log_click_to_fastapi(short_code, user_agent, ip_address):
    """Send click log to FastAPI."""
    log_data = {
        "short_code": short_code,
        "user_agent": user_agent,
        "ip_address": ip_address,
    }
    
    # Send the log to FastAPI
    try:
        response = requests.post('http://fastapi_service/click/', json=log_data)
        return response.status_code
    except Exception as e:
        print(f"Error sending log to FastAPI: {e}")
