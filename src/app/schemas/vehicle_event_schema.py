from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, StrictInt, field_validator


class VehicleEventStatusMixin(BaseModel):
    status: StrictInt | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is None or value in {0, 1, 2}:
            return value

        raise ValueError("Invalid vehicle event status")


class VehicleEventCreate(VehicleEventStatusMixin):
    camera_id: int
    plate: str | None = None
    event_type: str
    vehicle_type_id: int | None = None
    vehicle_confidence: float | None = None
    plate_confidence: float | None = None
    image_path: str | None = None
    plate_image_path: str | None = None
    bbox: dict[str, Any] | None = None


class VehicleEventReview(VehicleEventStatusMixin):
    plate: str | None = None
    vehicle_type_id: int | None = None
    reject_reason: str | None = None


class VehicleEventUpdate(VehicleEventStatusMixin):
    plate: str | None = None
    vehicle_type_id: int | None = None


class VehicleEventResponse(VehicleEventCreate):
    id: int
    event_time: datetime
    model_config = ConfigDict(
        from_attributes=True
    )


class VehicleEventPage(BaseModel):
    items: list[VehicleEventResponse]
    total: int
    skip: int = 0
    limit: int | None = None
