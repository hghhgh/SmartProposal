from collections import defaultdict
from datetime import datetime

events = []

def log_event(event_type: str, data: dict):
    events.append({
        "type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_events():
    return events
