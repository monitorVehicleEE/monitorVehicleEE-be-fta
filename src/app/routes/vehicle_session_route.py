from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.vehicle_session_repo import VehicleSessionRepository
from src.app.schemas.vehicle_session_schema import (
    VehicleSessionClose,
    VehicleSessionCreate,
    VehicleSessionResponse
)
from src.app.services.vehicle_session_service import VehicleSessionService


router = APIRouter(
    prefix="/vehicle-sessions",
    tags=["Vehicle Sessions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return VehicleSessionService(VehicleSessionRepository(db))


@router.get("", response_model=list[VehicleSessionResponse])
def get_vehicle_sessions(
    plate: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int | None = None,
    db=Depends(get_db)
):
    return get_service(db).find_all(
        plate=plate,
        status=status,
        skip=skip,
        limit=limit
    )


@router.get("/open/{plate}")
def get_open_session(plate: str, db=Depends(get_db)):
    session = get_service(db).get_open_session(plate)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Open vehicle session not found"
        )

    return session


@router.post("")
def create_vehicle_session(
    request: VehicleSessionCreate,
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{plate}/close")
def close_vehicle_session(
    plate: str,
    request: VehicleSessionClose,
    db=Depends(get_db)
):
    try:
        return get_service(db).close_session(
            plate=plate,
            out_event_id=request.out_event_id,
            out_camera_id=request.out_camera_id,
            out_time=request.out_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
