from pydantic import BaseModel, Field


class TempReadingDetail(BaseModel):
    """Finer metrics detail for temperature readings."""
    raw: float
    filtered: float
    trend_avg: float
    quality: str = Field(..., description="E.g., 'good', 'sensor_error', 'missing'")
    error: bool


class HumidityReadingDetail(BaseModel):
    """Finer metrics detail for humidity readings."""
    raw: float
    quality: str
    error: bool


class ReadingsContainer(BaseModel):
    """Aggregate payload container for temperature and moisture metrics."""
    temperature_c: TempReadingDetail
    humidity_pct: HumidityReadingDetail


class TelemetryPayload(BaseModel):
    """Complete incoming telemetry packet from ESP32 firmware."""
    device_id: str = Field(..., min_length=1)
    firmware_version: str
    schema_version: int
    timestamp: int = Field(..., description="Unix timestamp of sensor reading")
    readings: ReadingsContainer
    status: str = Field(..., description="Compost FSM state")
    quality_flag: str
    cycle_age_days: float
    battery_pct: int = Field(None, ge=0, le=100)
