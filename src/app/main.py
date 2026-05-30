from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.app.core.database import SessionLocal

from src.app.repositories.user_repository import UserRepository
from src.app.repositories.otp_repository import OTPRepository

from src.app.services.auth_service import AuthService
from src.app.services.otp_service import OTPService
from src.app.services.email_service import EmailService

from src.app.schemas.auth_schema import (
    RegisterRequest,
    ConfirmRegisterRequest,
    LoginRequest,
    SendOTPRequest
)
from src.app.routes.access_rule_route import router as access_rule_router
from src.app.routes.camera_route import router as camera_router
from src.app.routes.statistic_route import router as statistic_router
from src.app.routes.user_route import router as user_router
from src.app.routes.vehicle_event_route import router as vehicle_event_router
from src.app.routes.vehicle_route import router as vehicle_router
from src.app.routes.vehicle_session_route import router as vehicle_session_router
from src.app.routes.vehicle_type_route import router as vehicle_type_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
main = app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(access_rule_router)
app.include_router(camera_router)
app.include_router(statistic_router)
app.include_router(user_router)
app.include_router(vehicle_event_router)
app.include_router(vehicle_router)
app.include_router(vehicle_session_router)
app.include_router(vehicle_type_router)

def error_response(message: str, status_code: int):

    return JSONResponse(
        status_code=status_code,
        content={
            "message": message
        }
    )

# =========================================================
# DATABASE
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================================================
# SERVICES
# =========================================================

def get_auth_service(db: Session):

    user_repository = UserRepository(db)

    otp_repository = OTPRepository(db)

    otp_service = OTPService()

    email_service = EmailService()

    return AuthService(
        user_repository=user_repository,
        otp_repository=otp_repository,
        otp_service=otp_service,
        email_service=email_service
    )

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Backend API running"
    }

# =========================================================
# SEND OTP
# =========================================================

@app.post("/auth/send-otp")
def send_otp(
    request: SendOTPRequest,
    db: Session = Depends(get_db)
):

    try:

        auth_service = get_auth_service(db)

        result = auth_service.send_register_otp(request)

        return result

    except Exception as e:

        return error_response(str(e), 400)

# =========================================================
# REGISTER
# =========================================================

@app.post("/auth/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    try:

        auth_service = get_auth_service(db)

        result = auth_service.register(request)

        return result

    except Exception as e:

        return error_response(str(e), 400)

# =========================================================
# CONFIRM REGISTER
# =========================================================

@app.post("/auth/confirm-register")
def confirm_register(
    request: ConfirmRegisterRequest,
    db: Session = Depends(get_db)
):

    try:

        auth_service = get_auth_service(db)

        result = auth_service.confirm_register(request)

        return result

    except Exception as e:

        return error_response(str(e), 400)

# =========================================================
# LOGIN
# =========================================================

@app.post("/auth/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    try:

        auth_service = get_auth_service(db)

        result = auth_service.login(request)

        return result

    except Exception as e:

        return error_response(str(e), 401)
