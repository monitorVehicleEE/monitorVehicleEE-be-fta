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
def get_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    db=Depends(get_db)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    today_count = _count_events_from(db, today)
    week_count = _count_events_from(db, week_start)
    month_count = _count_events_from(db, month_start)
    range_start = start_date or today
    range_end = end_date or today
    range_count = _count_events_between(db, range_start, range_end)
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
        "range_total": range_count,
        "range_start": range_start,
        "range_end": range_end,
        "active_cameras": active_cameras,
        "total_cameras": total_cameras
    }


@router.get("/daily")
def get_daily(
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 7,
    group_by: str = "day",
    db=Depends(get_db)
):
    if end_date is None:
        end_date = date.today()

    if start_date is None:
        days = max(limit, 1)
        start_date = end_date - timedelta(days=days - 1)
    else:
        days = max((end_date - start_date).days + 1, 1)

    if group_by == "month":
        month_expr = func.date_trunc("month", VehicleEvent.event_time).label("event_month")
        rows = (
            db.query(
                month_expr,
                VehicleEvent.vehicle_type_id,
                func.count(VehicleEvent.id)
            )
            .filter(func.date(VehicleEvent.event_time) >= start_date)
            .filter(func.date(VehicleEvent.event_time) <= end_date)
            .filter(VehicleEvent.status != "PENDING")
            .group_by(
                month_expr,
                VehicleEvent.vehicle_type_id
            )
            .all()
        )

        stats = {}
        current_month = start_date.replace(day=1)
        end_month = end_date.replace(day=1)

        while current_month <= end_month:
            key = current_month.strftime("%Y-%m")
            stats[key] = {
                "date": key,
                "total": 0,
                "by_type": {}
            }

            if current_month.month == 12:
                current_month = current_month.replace(
                    year=current_month.year + 1,
                    month=1
                )
            else:
                current_month = current_month.replace(month=current_month.month + 1)

        for event_month, vehicle_type_id, count in rows:
            key = event_month.strftime("%Y-%m")
            type_key = vehicle_type_id or "unknown"
            stats[key]["total"] += count
            stats[key]["by_type"][type_key] = count

        return list(stats.values())

    rows = (
        db.query(
            func.date(VehicleEvent.event_time).label("event_date"),
            VehicleEvent.vehicle_type_id,
            func.count(VehicleEvent.id)
        )
        .filter(func.date(VehicleEvent.event_time) >= start_date)
        .filter(func.date(VehicleEvent.event_time) <= end_date)
        .filter(VehicleEvent.status != "PENDING")
        .group_by(
            func.date(VehicleEvent.event_time),
            VehicleEvent.vehicle_type_id
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

    for event_date, vehicle_type_id, count in rows:
        key = event_date.isoformat()
        type_key = vehicle_type_id or "unknown"
        stats[key]["total"] += count
        stats[key]["by_type"][type_key] = count

    return list(stats.values())


@router.get("/by-type")
def get_by_type(
    start_date: date | None = None,
    end_date: date | None = None,
    db=Depends(get_db)
):
    query = (
        db.query(
            VehicleEvent.vehicle_type_id,
            func.count(VehicleEvent.id)
        )
    )

    if start_date is not None:
        query = query.filter(func.date(VehicleEvent.event_time) >= start_date)

    if end_date is not None:
        query = query.filter(func.date(VehicleEvent.event_time) <= end_date)

    query = query.filter(VehicleEvent.status != "PENDING")

    rows = (
        query
        .group_by(VehicleEvent.vehicle_type_id)
        .all()
    )

    return [
        {
            "vehicle_type_id": vehicle_type_id,
            "vehicle_type": vehicle_type_id or "unknown",
            "count": count
        }
        for vehicle_type_id, count in rows
    ]


@router.get("/hourly")
def get_hourly(target_date: date | None = None, db=Depends(get_db)):
    if target_date is None:
        target_date = date.today()

    rows = (
        db.query(
            func.extract("hour", VehicleEvent.event_time).label("hour"),
            func.count(VehicleEvent.id)
        )
        .filter(func.date(VehicleEvent.event_time) == target_date)
        .filter(VehicleEvent.status != "PENDING")
        .group_by(func.extract("hour", VehicleEvent.event_time))
        .all()
    )

    stats = {
        hour: {
            "hour": f"{hour:02d}:00",
            "total": 0
        }
        for hour in range(24)
    }

    for event_hour, count in rows:
        stats[int(event_hour)]["total"] = count

    return list(stats.values())


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
        .filter(VehicleEvent.status != "PENDING")
        .scalar()
    )


def _count_events_between(db, start_date: date, end_date: date):
    return (
        db.query(func.count(VehicleEvent.id))
        .filter(func.date(VehicleEvent.event_time) >= start_date)
        .filter(func.date(VehicleEvent.event_time) <= end_date)
        .filter(VehicleEvent.status != "PENDING")
        .scalar()
    )
