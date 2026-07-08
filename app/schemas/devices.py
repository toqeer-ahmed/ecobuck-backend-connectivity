from datetime import datetime
from pydantic import BaseModel, Field


class DeviceClaim(BaseModel):
    """Payload to claim ownership of pre-provisioned physical hardware."""
    hardware_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1, max_length=50)


class DeviceConfigUpdate(BaseModel):
    """Payload to configure dynamic parameters of a device."""
    temp_offset_c: float = Field(None, ge=-10.0, le=10.0)
    humidity_offset_pct: float = Field(None, ge=-20.0, le=20.0)
    read_interval_seconds: int = Field(None, ge=10, le=3600)
    summary_interval_seconds: int = Field(None, ge=30, le=86400)


class DeviceResponse(BaseModel):
    """Schema representing current device metadata and status details."""
    device_id: str
    label: str
    status: str
    firmware_version: str
    last_seen: datetime = None
    battery_pct: int = None
