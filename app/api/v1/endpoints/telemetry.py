import time
from fastapi import APIRouter, Depends, status
from app.schemas.telemetry import TelemetryPayload
from app.repositories.telemetry import TelemetryRepository
from app.repositories.device import DeviceRepository
from app.api.deps import verify_device_token

router = APIRouter()


@router.post("/telemetry", status_code=status.HTTP_202_ACCEPTED, tags=["Telemetry Ingestion"])
async def ingest_telemetry(
    payload: TelemetryPayload,
    x_device_token: str = Depends(verify_device_token),
    telemetry_repo: TelemetryRepository = Depends(TelemetryRepository),
    device_repo: DeviceRepository = Depends(DeviceRepository),
):
    """
    Ingest a telemetry packet from the ESP32 hardware device.
    Saves to the time-series telemetry subcollection and updates the latest status cached document.
    """

    # 1. Save time-series log
    telemetry_data = payload.model_dump()
    telemetry_repo.add_telemetry_reading(payload.device_id, telemetry_data)

    # 2. Setup latest status cache package
    latest_status_payload = {
        "timestamp": payload.timestamp,
        "temp": payload.readings.temperature_c.filtered,
        "humidity": payload.readings.humidity_pct.raw,
        "status": payload.status,
        "qualityFlag": payload.quality_flag,
        "cycleAgeDays": payload.cycle_age_days,
        "batteryPct": payload.battery_pct,
    }

    # 3. Update device document status and write cache document `/latest/status`
    device_repo.update_status(payload.device_id, payload.status)
    device_repo.update_latest_status(payload.device_id, latest_status_payload)

    return {
        "status": "success",
        "message": "Telemetry accepted",
        "timestamp": int(time.time())
    }
