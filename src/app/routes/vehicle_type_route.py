from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.vehicle_type_repo import VehicleTypeRepository
from src.app.schemas.vehicle_type_schema import VehicleTypeCreate
from src.app.services.vehicle_type_service import VehicleTypeService


router = APIRouter(
    prefix="/vehicle-types",
    tags=["Vehicle Types"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return VehicleTypeService(VehicleTypeRepository(db))


@router.get("")
def get_vehicle_types(db=Depends(get_db)):
    return get_service(db).get_all()


@router.get("/{type_id}")
def get_vehicle_type(type_id: int, db=Depends(get_db)):
    try:
        return get_service(db).get_by_id(type_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("")
def create_vehicle_type(
    request: VehicleTypeCreate,
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

