from fastapi import APIRouter, HTTPException
from app.schemas.event_schema import RawEvent
from app.core.event_store import add_event
from app.core.normalization import normalize_event
from app.risk.engine import RiskEngine
from app.risk.config import PolicyManager
from app.correlation.engine import CorrelationEngine
from app.detection.engine import DetectionEngine
from app.detection.context import DetectionContext

router = APIRouter()

policy_manager = PolicyManager("app/risk/policy.json")
policy_manager.load_policy()

risk_engine = RiskEngine(policy_manager)
correlation_engine = CorrelationEngine()

detection_context = DetectionContext()
detection_engine = DetectionEngine(detection_context)


@router.post("/ingest")
def ingest_event(event: RawEvent):
    normalized_event = normalize_event(event)

    enriched_event = risk_engine.apply(normalized_event)

    correlated_event = correlation_engine.apply(enriched_event)

    detection_context.add_event(correlated_event)
    detection_result = detection_engine.run(correlated_event)

    correlated_event["detection"] = detection_result

    added = add_event(correlated_event)

    if not added:
        raise HTTPException(
            status_code=406,
            detail="Duplicate event_id. Event ignored."
        )

    return {
        "status": "success",
        "message": "Event ingested successfully",
        "event_id": event.event_id,
        "risk": correlated_event["risk"],
        "correlation": correlated_event.get("correlation", None),
        "detection": correlated_event["detection"]
    } 
