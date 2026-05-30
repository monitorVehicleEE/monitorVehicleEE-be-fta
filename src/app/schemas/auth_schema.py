# validate request
# response format
# serialize JSON

from pydantic import BaseModel, EmailStr
from typing import Optional


# =========================================================
# SEND OTP
# =========================================================

class SendOTPRequest(BaseModel):

    email   : EmailStr


# =========================================================
# REGISTER
# =========================================================

class RegisterRequest(BaseModel):
    username: str
    email   : EmailStr
    password: str

class ConfirmRegisterRequest(BaseModel):
    username: str
    email   : EmailStr
    password: str
    otp: str
    fullname: Optional[str] = None


# =========================================================
# LOGIN
# =========================================================

class LoginRequest(BaseModel):
    username: str
    password: str


# =========================================================
# USER RESPONSE
# =========================================================

class UserResponse(BaseModel):
    id      : int
    username: str
    email   : str
    class Config:
        from_attributes = True
