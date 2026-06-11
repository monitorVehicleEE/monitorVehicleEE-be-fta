from fastapi import APIRouter, Depends, HTTPException

from src.app.core.database import SessionLocal
from src.app.repositories.acess_rule_repo import AccessRuleRepository
from src.app.repositories.vehicle_repo import VehicleRepository
from src.app.schemas.access_rule_schema import (
    AccessRuleCreate,
    AccessRuleResponse,
    AccessRuleUpdate
)
from src.app.services.access_rule_service import AccessRuleService


router = APIRouter(
    prefix="/access-rules",
    tags=["Access Rules"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db):
    return AccessRuleService(
        AccessRuleRepository(db),
        VehicleRepository(db)
    )


@router.get("", response_model=list[AccessRuleResponse])
def get_access_rules(db=Depends(get_db)):
    return get_service(db).get_all()


@router.get("/plate/{plate}", response_model=list[AccessRuleResponse])
def get_access_rules_by_plate(
    plate: str,
    db=Depends(get_db)
):
    return get_service(db).get_by_plate(plate)


@router.get("/{rule_id}", response_model=AccessRuleResponse)
def get_access_rule(rule_id: int, db=Depends(get_db)):
    try:
        return get_service(db).get_by_id(rule_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=AccessRuleResponse, status_code=201)
def create_access_rule(
    request: AccessRuleCreate,
    db=Depends(get_db)
):
    try:
        return get_service(db).create(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{rule_id}", response_model=AccessRuleResponse)
def update_access_rule(
    rule_id: int,
    request: AccessRuleUpdate,
    db=Depends(get_db)
):
    try:
        return get_service(db).update(rule_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{rule_id}", response_model=AccessRuleResponse)
def delete_access_rule(rule_id: int, db=Depends(get_db)):
    try:
        return get_service(db).delete(rule_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
