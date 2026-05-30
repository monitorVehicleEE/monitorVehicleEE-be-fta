from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleTypeCreate(BaseModel):
    code: str
    name: str
    description: str | None = None


class VehicleTypeResponse(VehicleTypeCreate):
    id: int
    status: int
    date_new: datetime
    model_config = ConfigDict(from_attributes=True)

