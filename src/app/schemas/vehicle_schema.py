from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    plate: str
    vehicle_type: str | None = None
    is_internal: bool = False

class VehicleUpdate(BaseModel):
    plate: str | None = None
    vehicle_type: str | None = None
    is_internal: bool | None = None

class VehicleResponse(VehicleCreate):
    id: int
    status: int
    date_new: datetime
    model_config = ConfigDict(from_attributes=True)
