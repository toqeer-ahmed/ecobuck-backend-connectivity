from fastapi import APIRouter

# Root API router representing the v1 endpoint namespace
api_router = APIRouter(prefix="/api/v1")

# Endpoint routers (auth, telemetry, devices, alerts) will be registered here
# during their respective incremental module implementation steps.
