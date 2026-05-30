# decode JWT
# lấy current user
# protect API

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from src.app.core.security import SecurityService

# Endpoint login để lấy token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthDependency:
    @staticmethod
    def get_current_user( token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token,
                SecurityService.SECRET_KEY,
                algorithms=[SecurityService.ALGORITHM]
            )
            user_id = payload.get("user_id")
            username = payload.get("sub")
            user_type = payload.get("type")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

            return {
                "user_id": user_id,
                "username": username,
                "type": user_type
            }
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired"
            )
