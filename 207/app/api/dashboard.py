from fastapi import APIRouter, Depends
from app.core.security import require_admin
from app.core.security_events import get_events

router = APIRouter()

@router.get("/")
def dashboard(role=Depends(require_admin)):
    events = get_events()

    return {
        "total_events": len(events),
        "dependency_alerts": [
            e for e in events if e["type"] == "DEPENDENCY_VULNERABILITY"
        ],
        "all_events": events
    }
