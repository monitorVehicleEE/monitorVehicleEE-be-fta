from datetime import date

from pydantic import BaseModel


class DailyStatistic(BaseModel):
    date: date
    total: int
    by_type: dict[str, int]


class TypeStatistic(BaseModel):
    vehicle_type: str
    count: int


class SummaryStatistic(BaseModel):
    today: int
    this_week: int
    this_month: int
    active_cameras: int
    total_cameras: int
