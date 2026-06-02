from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleSessionCreate(BaseModel):
    plate: str | None = None
    in_event_id: int | None = None
    out_event_id: int | None = None
    in_camera_id: int | None = None
    out_camera_id: int | None = None
    in_time: datetime | None = None
    out_time: datetime | None = None
    duration_seconds: int | None = None
    status: str | None = None


class VehicleSessionClose(BaseModel):
    out_event_id: int | None = None
    out_camera_id: int | None = None
    out_time: datetime | None = None


class VehicleSessionResponse(BaseModel):
    id: int
    plate: str | None
    in_time: datetime
    out_time: datetime | None
    duration_seconds: int | None
    status: str
    model_config = ConfigDict(
        from_attributes=True
    )

