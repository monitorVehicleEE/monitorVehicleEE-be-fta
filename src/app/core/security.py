# hash password
# verify password
# JWT token

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

class SecurityService:

    SECRET_KEY = "MN@81*4"

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

    @staticmethod
    def hash_password(password: str):

        return SecurityService.pwd_context.hash(
            password
        )

    @staticmethod
    def verify_password( plain_password: str, hashed_password: str ):

        return (
            SecurityService.pwd_context.verify(
                plain_password,
                hashed_password
            )
        )

    @staticmethod
    def create_access_token(data: dict):

        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=SecurityService.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({
            "exp": expire
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SecurityService.SECRET_KEY,
            algorithm=SecurityService.ALGORITHM
        )

        return encoded_jwt
