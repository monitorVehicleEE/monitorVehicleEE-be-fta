from fastapi import APIRouter, Depends, HTTPException

from src.app.dependencies.auth_dependency import AuthDependency

from src.app.repositories.user_repository import UserRepository

from src.app.services.user_service import UserService

from src.app.core.database import SessionLocal

from src.app.schemas.user_schema import UserUpdateRequest


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# /me - lấy thông tin user hiện tại
@router.get("/me")
def get_me(
    current_user=Depends(AuthDependency.get_current_user),
    db=Depends(get_db)
):

    repository = UserRepository(db)
    service = UserService(repository)

    return service.get_user(current_user["user_id"])


# update profile
@router.put("/me")
def update_me(
    request: UserUpdateRequest,
    current_user=Depends(AuthDependency.get_current_user),
    db=Depends(get_db)
):

    try:
        repository = UserRepository(db)
        service = UserService(repository)

        updated_user = service.update_profile(
            current_user["user_id"],
            request
        )

        return {
            "message": "Update profile success",
            "user": updated_user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
