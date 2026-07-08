from datetime import datetime
from pydantic import BaseModel


class AlertResponse(BaseModel):
    """Schema representing alert events triggered by the rules engine."""
    alert_id: str
    device_id: str
    alert_type: str
    message: str
    resolved: bool
    triggered_at: datetime
    resolved_at: datetime = None


class AlertResolveResponse(BaseModel):
    """Response returned upon successfully acknowledging an alert."""
    alert_id: str
    resolved: bool
    resolved_at: datetime
