from fastapi import APIRouter
from app.api.v1.endpoints.telemetry import router as telemetry_router
from app.api.v1.endpoints.devices import router as devices_router
from app.api.v1.endpoints.alerts import router as alerts_router

# Root API router representing the v1 endpoint namespace
api_router = APIRouter(prefix="/api/v1")

# Include sub-routers
api_router.include_router(telemetry_router)
api_router.include_router(devices_router)
api_router.include_router(alerts_router)


