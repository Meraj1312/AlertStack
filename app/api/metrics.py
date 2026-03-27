from fastapi import APIRouter
from datetime import datetime
from typing import Optional

from app.core.event_store import query_events
from app.core.alert_builder import build_alerts_from_events

router = APIRouter()


@router.get("/metrics")
def get_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
):
    events = query_events(
        start_time=start_time,
        end_time=end_time,
    )

    alerts = build_alerts_from_events(events)

    total_events = len(events)
    total_alerts = len(alerts)

    high_severity_alerts = len([
        a for a in alerts if a.get("severity") in ["high", "critical"]
    ])

    severity_breakdown = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    for e in events:
        sev = e.get("risk", {}).get("severity")
        if sev in severity_breakdown:
            severity_breakdown[sev] += 1

    event_type_breakdown = {}

    for e in events:
        etype = e.get("event_type", "unknown")
        event_type_breakdown[etype] = event_type_breakdown.get(etype, 0) + 1

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "high_severity_alerts": high_severity_alerts,
        "severity_breakdown": severity_breakdown,
        "event_type_breakdown": event_type_breakdown
    }
