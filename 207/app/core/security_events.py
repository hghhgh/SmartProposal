from datetime import datetime

SECURITY_EVENTS = []

def log_event(event_type: str, details: dict):
    SECURITY_EVENTS.append({
        "type": event_type,
        "details": details,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_events():
    return SECURITY_EVENTS
