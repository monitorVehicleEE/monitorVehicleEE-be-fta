from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.vehicle_event_repo import VehicleEventRepository
from src.app.schemas.vehicle_event_schema import (
    VehicleEventCreate,
    VehicleEventResponse,
    VehicleEventReview,
    VehicleEventUpdate
)
from src.app.services.vehicle_event_service import VehicleEventService


router = APIRouter(
    prefix="/vehicle-events",
    tags=["Vehicle Events"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return VehicleEventService(VehicleEventRepository(db))


@router.get("", response_model=list[VehicleEventResponse])
def get_vehicle_events(
    camera_id: int | None = None,
    vehicle_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    skip: int = 0,
    limit: int | None = None,
    db=Depends(get_db)
):
    return get_service(db).find_history(
        camera_id=camera_id,
        vehicle_type=vehicle_type,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )


@router.get("/live-feed")
def get_live_feed(
    camera_id: int | None = None,
    db=Depends(get_db)
):
    return get_service(db).live_feed(camera_id=camera_id)


@router.get("/pending")
def get_pending_events(
    limit: int = 20,
    camera_id: int | None = None,
    db=Depends(get_db)
):
    return get_service(db).find_pending(
        limit=limit,
        camera_id=camera_id
    )


@router.get("/plate/{plate}", response_model=list[VehicleEventResponse])
def get_events_by_plate(plate: str, db=Depends(get_db)):
    return get_service(db).find_by_plate(plate)


@router.get("/plate/{plate}/latest")
def get_latest_event_by_plate(plate: str, db=Depends(get_db)):
    event = get_service(db).find_latest_by_plate(plate)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Vehicle event not found"
        )

    return event


@router.post("")
def create_vehicle_event(
    request: VehicleEventCreate,
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{event_id}")
def update_vehicle_event(
    event_id: int,
    request: VehicleEventUpdate,
    db=Depends(get_db)
):
    try:
        return get_service(db).update(event_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{event_id}/approve")
def approve_vehicle_event(
    event_id: int,
    request: VehicleEventReview,
    db=Depends(get_db)
):
    try:
        return get_service(db).approve(event_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{event_id}/reject")
def reject_vehicle_event(
    event_id: int,
    request: VehicleEventReview,
    db=Depends(get_db)
):
    try:
        return get_service(db).reject(event_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
