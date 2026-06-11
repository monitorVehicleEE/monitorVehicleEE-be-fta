from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.dependencies.auth_dependency import AuthDependency
from src.app.repositories.vehicle_repo import VehicleRepository
from src.app.repositories.vehicle_type_repo import VehicleTypeRepository
from src.app.schemas.vehicle_schema import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate
)
from src.app.services.vehicle_service import VehicleService


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return VehicleService(
        VehicleRepository(db),
        VehicleTypeRepository(db)
    )


@router.get("")
def get_vehicles(
    limit: int | None = None,
    db=Depends(get_db)
):
    vehicles = get_service(db).get_all()

    if limit is not None:
        return vehicles[:limit]

    return vehicles


@router.get("/plate/{plate}", response_model=VehicleResponse)
def get_vehicle_by_plate(
    plate: str,
    db=Depends(get_db)
):
    try:
        return get_service(db).get_by_plate(plate)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db=Depends(get_db)
):
    try:
        return get_service(db).get_by_id(vehicle_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=VehicleResponse, status_code=201)
def create_vehicle(
    request: VehicleCreate,
    current_user=Depends(AuthDependency.require_admin),
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    request: VehicleUpdate,
    current_user=Depends(AuthDependency.require_admin),
    db=Depends(get_db)
):
    try:
        return get_service(db).update(vehicle_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
