from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime

from app.core.event_store import query_events

router = APIRouter()


@router.get("/events")
def get_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = Query(None, regex="^(low|medium|high|critical)$"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
):
    if start_time and end_time and start_time > end_time:
        return {"total": 0, "events": []}

    results = query_events(
        user_id=user_id,
        event_type=event_type,
        severity=severity,
        start_time=start_time,
        end_time=end_time,
    )

    paginated = results[offset: offset + limit]

    return {
        "total": len(results),
        "filters": {
            "user_id": user_id,
            "event_type": event_type,
            "severity": severity
        },
        "events": paginated
    } 
