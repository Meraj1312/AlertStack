from fastapi import APIRouter
from typing import Optional
from datetime import datetime

from app.core.event_store import query_events

router = APIRouter()


@router.get("/users/{user_id}/activity")
def get_user_activity(
    user_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
):
    events = query_events(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
    )

   
    events.sort(key=lambda x: x["timestamp"])

    timeline = events[:limit]

    return {
        "user_id": user_id,
        "total_events": len(events),
        "timeline": timeline
    }
