from fastapi import FastAPI
from app.api.ingestion import router
from app.core.event_store import get_all_events

app = FastAPI()

app.include_router(router)


@app.get("/events")
def get_events():
    events = get_all_events()
    return {
        "count": len(events),
        "events": events
    } 
