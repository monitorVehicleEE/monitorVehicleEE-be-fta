from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    vehicle_event_id: int
    access_rule_id: int | None = None
    plate: str
    camera_id: int
    alert_type: str
    severity: str = "high"
    message: str
    image_path: str | None = None
    plate_image_path: str | None = None


class AlertResponse(AlertCreate):
    id: int
    status: int
    is_resolved: bool
    resolved_by: str | None = None
    resolved_at: datetime | None = None
    timestamp: datetime | None = None
    vehicle_id: int | None = None
    date_new: datetime
    model_config = ConfigDict(from_attributes=True)
