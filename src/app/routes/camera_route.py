from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.dependencies.auth_dependency import AuthDependency
from src.app.repositories.camera_repo import CameraRepository
from src.app.schemas.camera_schema import CameraCreate, CameraUpdate
from src.app.services.camera_service import CameraService


router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return CameraService(CameraRepository(db))


@router.get("")
def get_cameras(db=Depends(get_db)):
    return get_service(db).get_all()


@router.get("/{camera_id}")
def get_camera(camera_id: int, db=Depends(get_db)):
    try:
        return get_service(db).get_by_id(camera_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("")
def create_camera(
    request: CameraCreate,
    current_user=Depends(AuthDependency.require_admin),
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{camera_id}")
def update_camera(
    camera_id: int,
    request: CameraUpdate,
    current_user=Depends(AuthDependency.require_admin),
    db=Depends(get_db)
):
    try:
        return get_service(db).update(camera_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
