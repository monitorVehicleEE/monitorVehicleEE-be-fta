from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.vehicle_event_repo import VehicleEventRepository
from src.app.schemas.vehicle_event_schema import VehicleEventCreate
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


@router.get("/plate/{plate}")
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

