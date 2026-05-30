from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CameraCreate(BaseModel):
    code: str | None = None
    name: str
    location: str | None = None
    camera_role: int  # 0: entry, 1: exit, 2: internal
    source_type: str  # file | rtsp | http
    source_path: str

class CameraUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    location: str | None = None
    camera_role: int | None = None
    source_type: str | None = None
    source_path: str | None = None
    status: int | None = None

class CameraResponse(CameraCreate):
    id: int
    status: int
    date_new: datetime
    model_config = ConfigDict(from_attributes=True)
