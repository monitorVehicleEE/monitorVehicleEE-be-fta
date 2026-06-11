from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.alert_repo import AlertRepository
from src.app.schemas.alert_schema import AlertCreate, AlertResponse
from src.app.services.alert_service import AlertService


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return AlertService(AlertRepository(db))


@router.get("", response_model=list[AlertResponse])
def get_alerts(
    is_resolved: bool | None = None,
    db=Depends(get_db)
):
    return get_service(db).get_all(is_resolved=is_resolved)


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db=Depends(get_db)):
    try:
        return get_service(db).get_by_id(alert_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(request: AlertCreate, db=Depends(get_db)):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    resolved_by: str | None = None,
    db=Depends(get_db)
):
    try:
        return get_service(db).resolve(alert_id, resolved_by=resolved_by)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{alert_id}", response_model=AlertResponse)
def delete_alert(alert_id: int, db=Depends(get_db)):
    try:
        return get_service(db).delete(alert_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
