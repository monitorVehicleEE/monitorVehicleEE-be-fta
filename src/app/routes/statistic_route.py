from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func

from src.app.core.database import SessionLocal
from src.app.models.camera_model import Camera
from src.app.models.vehicle_event_model import VehicleEvent


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_summary(db=Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    today_count = _count_events_from(db, today)
    week_count = _count_events_from(db, week_start)
    month_count = _count_events_from(db, month_start)
    total_cameras = db.query(Camera).count()
    active_cameras = (
        db.query(Camera)
        .filter(Camera.status == 1)
        .count()
    )

    return {
        "today": today_count,
        "this_week": week_count,
        "this_month": month_count,
        "active_cameras": active_cameras,
        "total_cameras": total_cameras
    }


@router.get("/daily")
def get_daily(limit: int = 7, db=Depends(get_db)):
    days = max(limit, 1)
    start_date = date.today() - timedelta(days=days - 1)

    rows = (
        db.query(
            func.date(VehicleEvent.event_time).label("event_date"),
            VehicleEvent.vehicle_type,
            func.count(VehicleEvent.id)
        )
        .filter(func.date(VehicleEvent.event_time) >= start_date)
        .group_by(
            func.date(VehicleEvent.event_time),
            VehicleEvent.vehicle_type
        )
        .all()
    )

    stats = {}

    for index in range(days):
        current_date = start_date + timedelta(days=index)
        stats[current_date.isoformat()] = {
            "date": current_date.isoformat(),
            "total": 0,
            "by_type": {}
        }

    for event_date, vehicle_type, count in rows:
        key = event_date.isoformat()
        type_key = vehicle_type or "unknown"
        stats[key]["total"] += count
        stats[key]["by_type"][type_key] = count

    return list(stats.values())


@router.get("/by-type")
def get_by_type(db=Depends(get_db)):
    rows = (
        db.query(
            VehicleEvent.vehicle_type,
            func.count(VehicleEvent.id)
        )
        .group_by(VehicleEvent.vehicle_type)
        .all()
    )

    return [
        {
            "vehicle_type": vehicle_type or "unknown",
            "count": count
        }
        for vehicle_type, count in rows
    ]


@router.get("/camera/{camera_id}")
def get_by_camera(camera_id: int, db=Depends(get_db)):
    return (
        db.query(VehicleEvent)
        .filter(VehicleEvent.camera_id == camera_id)
        .order_by(VehicleEvent.event_time.desc())
        .all()
    )


def _count_events_from(db, start_date: date):
    return (
        db.query(func.count(VehicleEvent.id))
        .filter(func.date(VehicleEvent.event_time) >= start_date)
        .scalar()
    )
