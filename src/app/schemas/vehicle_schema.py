from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class VehicleCreate(BaseModel):
    plate: str
    owner_name: str | None = None
    owner_phone: str | None = None
    owner_cccd: str | None = None
    owner_address: str | None = None
    vehicle_type_id: int | None = None
    is_internal: bool = False

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, value):
        plate = value.strip().upper()
        if not plate:
            raise ValueError("Plate is required")
        return plate

class VehicleUpdate(BaseModel):
    plate: str | None = None
    owner_name: str | None = None
    owner_phone: str | None = None
    owner_cccd: str | None = None
    owner_address: str | None = None
    vehicle_type_id: int | None = None
    is_internal: bool | None = None

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, value):
        if value is None:
            return value

        plate = value.strip().upper()
        if not plate:
            raise ValueError("Plate is required")
        return plate

class VehicleResponse(VehicleCreate):
    id: int
    status: int
    date_new: datetime
    model_config = ConfigDict(from_attributes=True)
