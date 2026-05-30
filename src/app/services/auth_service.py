# Business logic

from src.app.core.security import SecurityService
from src.app.models.otp_model import OTP
from src.app.models.user_model import User
from src.app.repositories.otp_repository import OTPRepository
from src.app.repositories.user_repository import UserRepository
from src.app.services.email_service import EmailService
from src.app.services.otp_service import OTPService


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
        otp_repository: OTPRepository,
        otp_service: OTPService,
        email_service: EmailService
    ):
        self.user_repository = user_repository
        self.otp_repository = otp_repository
        self.otp_service = otp_service
        self.email_service = email_service

    def send_register_otp(self, request):
        email = str(request.email).strip().lower()

        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise Exception("Email đã tồn tại")

        otp_code = self.otp_service.generate_otp()
        otp = OTP(
            email=email,
            otp_code=otp_code,
            is_used=0,
            expire_at=self.otp_service.get_expire_time()
        )

        self.otp_repository.create(otp)
        self.email_service.send_otp_email(email, otp_code)

        return {
            "message": "Đã gửi OTP tới email"
        }

    def register(self, request):
        username = request.username.strip()
        email = str(request.email).strip().lower()

        self._validate_register_identity(username, email)

        otp_code = self.otp_service.generate_otp()
        otp = OTP(
            email=email,
            otp_code=otp_code,
            is_used=0,
            expire_at=self.otp_service.get_expire_time()
        )

        self.otp_repository.create(otp)
        self.email_service.send_otp_email(email, otp_code)

        return {
            "message": "Đã gửi OTP tới email"
        }

    def confirm_register(self, request):
        username = request.username.strip()
        email = str(request.email).strip().lower()

        self._validate_register_identity(username, email)

        otp = self.otp_repository.get_latest_by_email(email)
        if not otp:
            raise Exception("Chưa có OTP cho email này")

        if not self.otp_service.verify_otp(otp, request.otp):
            raise Exception("OTP không hợp lệ hoặc đã hết hạn")

        hashed_password = SecurityService.hash_password(request.password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            fullname=request.fullname,
            status=1,
            type=200
        )

        created_user = self.user_repository.create(user)

        otp.is_used = 1
        self.otp_repository.update(otp)

        return {
            "message": "Đăng ký thành công",
            "user_id": created_user.id
        }

    def login(self, request):
        user = self.user_repository.get_by_username(request.username)

        if not user:
            raise Exception("Tên đăng nhập không tồn tại")

        is_valid_password = SecurityService.verify_password(
            request.password,
            user.password
        )

        if not is_valid_password:
            raise Exception("Sai mật khẩu")

        access_token = SecurityService.create_access_token({
            "sub": user.username,
            "user_id": user.id,
            "type": user.type
        })

        return {
            "access_token": access_token,
            "token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "avatar": user.avatar,
                "type": user.type
            }
        }

    def _validate_register_identity(self, username: str, email: str):
        if not username:
            raise Exception("Vui lòng nhập username")

        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise Exception("Tên người dùng đã tồn tại")

        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise Exception("Email đã tồn tại")
