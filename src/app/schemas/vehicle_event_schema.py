from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class VehicleEventCreate(BaseModel):
    camera_id: int
    plate: str | None = None
    event_type: str
    vehicle_type_id: int | None = None
    vehicle_confidence: float | None = None
    plate_confidence: float | None = None
    image_path: str | None = None
    plate_image_path: str | None = None
    bbox: dict[str, Any] | None = None
    status: str | None = None


class VehicleEventReview(BaseModel):
    plate: str | None = None
    vehicle_type_id: int | None = None
    status: str | None = None
    reject_reason: str | None = None


class VehicleEventUpdate(BaseModel):
    plate: str | None = None
    vehicle_type_id: int | None = None
    status: str | None = None


class VehicleEventResponse(VehicleEventCreate):
    id: int
    event_time: datetime
    model_config = ConfigDict(
        from_attributes=True
    )
