from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime

from app.core.event_store import query_events
from app.core.alert_builder import build_alerts_from_events
from app.schemas.alert_response import AlertsAPIResponse

router = APIRouter()


@router.get("/alerts", response_model=AlertsAPIResponse)
def get_alerts(
    user_id: Optional[str] = None,
    severity: Optional[str] = Query(None, regex="^(low|medium|high|critical)$"),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
):
    
    events = query_events(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
    )

    
    alerts = build_alerts_from_events(events)

    
    if severity:
        alerts = [a for a in alerts if a.get("severity") == severity]

   
    paginated = alerts[offset: offset + limit]

    return {
        "total": len(alerts),
        "alerts": paginated
    }
