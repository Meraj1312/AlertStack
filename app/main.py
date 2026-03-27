from fastapi import FastAPI
from app.api.ingestion import router as ingestion_router
from app.api.events import router as events_router
from app.api.alerts import router as alerts_router
from app.api.users import router as users_router
from app.api.users import router as users_router

app = FastAPI()

app.include_router(ingestion_router)
app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(users_router)
app.include_router(users_router)
