from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers

app = FastAPI(
    title="EcoBuck Smart Compost Monitoring System API",
    description="Connectivity & Backend Services for ESP32 Firmware and Mobile Client Dashboard",
    version="1.0.0",
)

# Configure CORS Middleware for development/production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local simulators/testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include baseline v1 API routers
app.include_router(api_router)

# Register custom exception handlers globally
register_exception_handlers(app)



@app.get("/health", tags=["System Health"])
async def health_check():
    """
    Direct system health check route. Returns status and timestamp metadata.
    """
    import time
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "service": "ecobuck-backend"
    }
