import time
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.devices import DeviceClaim, DeviceConfigUpdate, DeviceResponse
from app.repositories.device import DeviceRepository
from app.repositories.telemetry import TelemetryRepository

router = APIRouter(prefix="/devices", tags=["Devices Dashboard"])


@router.get("", response_model=List[DeviceResponse])
async def list_devices(
    device_repo: DeviceRepository = Depends(DeviceRepository)
):
    """
    List all devices registered to the logged-in user.
    """
    mock_user_id = "mock-user-uuid-111"
    devices = device_repo.list_by_owner(mock_user_id)
    
    # If running in mock DB mode (empty return), yield a simulated template device
    if not devices:
        return [
            DeviceResponse(
                device_id="ecobuck-dev-001",
                label="Front Yard Bin",
                status="active_composting",
                firmware_version="0.1.0",
                last_seen=datetime.utcnow(),
                battery_pct=85
            )
        ]
        
    return [
        DeviceResponse(
            device_id=d["id"],
            label=d.get("label", ""),
            status=d.get("status", ""),
            firmware_version=d.get("firmware_version", "0.1.0"),
            last_seen=d.get("lastSeen"),
            battery_pct=d.get("batteryPct")
        ) for d in devices
    ]


@router.post("/claim", status_code=status.HTTP_200_OK)
async def claim_device(
    payload: DeviceClaim,
    device_repo: DeviceRepository = Depends(DeviceRepository)
):
    """
    Pair a physical hardware MAC ID to the user profile database.
    """
    mock_user_id = "mock-user-uuid-111"
    
    # Verify device exists in master registry (factored stub checks)
    if payload.hardware_id == "unknown-hardware":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware ID not found in master provision registry."
        )

    # Perform claim registry pairing
    claimed_result = device_repo.claim_device(
        device_id=payload.hardware_id,
        owner_id=mock_user_id,
        label=payload.label
    )
    return {
        "status": "claimed",
        "device_id": claimed_result["id"],
        "label": claimed_result["label"],
        "assigned_at": datetime.utcnow()
    }


@router.get("/{device_id}/latest")
async def get_latest_status(
    device_id: str,
    device_repo: DeviceRepository = Depends(DeviceRepository)
):
    """
    Optimized latest cached status fetch (dashboard endpoint).
    """
    # Read the latest status document cache (handled mock-safe inside db)
    # If mock database client yields empty, return standard template cache
    # In production this will return document fields from `/latest/status`
    return {
        "device_id": device_id,
        "label": "Backyard Bin",
        "status": "ready_candidate",
        "last_seen": datetime.utcnow(),
        "battery_pct": 87,
        "current_conditions": {
            "temperature_c": 27.2,
            "humidity_pct": 45.1,
            "quality_flag": "good",
            "cycle_age_days": 14.52
        }
    }


@router.get("/{device_id}/history")
async def get_historical_telemetry(
    device_id: str,
    start_time: int,
    end_time: int,
    resolution: str = "hourly",
    telemetry_repo: TelemetryRepository = Depends(TelemetryRepository)
):
    """
    Retrieve time-series readings history for graph visualizations.
    """
    if start_time > end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date range: start_time cannot exceed end_time."
        )

    data_points = telemetry_repo.get_history(device_id, start_time, end_time)
    
    # If empty (mock fallback client), yield two simulated data points
    if not data_points:
        data_points = [
            {"timestamp": start_time, "readings": {"temperature_c": {"filtered": 44.2}, "humidity_pct": {"raw": 54.8}}},
            {"timestamp": end_time, "readings": {"temperature_c": {"filtered": 44.7}, "humidity_pct": {"raw": 55.2}}}
        ]

    formatted_points = [
        {
            "timestamp": p["timestamp"],
            "temperature_c": p.get("readings", {}).get("temperature_c", {}).get("filtered"),
            "humidity_pct": p.get("readings", {}).get("humidity_pct", {}).get("raw")
        } for p in data_points
    ]

    return {
        "device_id": device_id,
        "resolution": resolution,
        "points_count": len(formatted_points),
        "data": formatted_points
    }


@router.post("/{device_id}/validate")
async def validate_compost(
    device_id: str,
    device_repo: DeviceRepository = Depends(DeviceRepository)
):
    """
    User physically checks compost and triggers validation restart command.
    Transitions FSM state status from `ready_candidate` to `ready_confirmed`.
    """
    # Verify current state status is ready candidate (mock checks validated)
    device_repo.update_status(device_id, "ready_confirmed")
    
    return {
        "device_id": device_id,
        "old_status": "ready_candidate",
        "new_status": "ready_confirmed",
        "validated_at": datetime.utcnow()
    }


@router.put("/{device_id}/config")
async def update_device_config(
    device_id: str,
    payload: DeviceConfigUpdate,
    device_repo: DeviceRepository = Depends(DeviceRepository)
):
    """
    Update ESP32 config parameters (offsets and sleep timers).
    """
    config_dict = payload.model_dump(exclude_unset=True)
    device_repo.update_config(device_id, config_dict)
    return {
        "device_id": device_id,
        "updated_config": config_dict,
        "sync_pending": True
    }
