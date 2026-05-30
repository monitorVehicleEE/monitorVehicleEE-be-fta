from sqlalchemy import Column, BigInteger, String, Integer, TIMESTAMP
from sqlalchemy.sql import func

from src.app.core.database import Base

from sqlalchemy import Column, BigInteger, String, Integer, TIMESTAMP
from sqlalchemy.sql import func

from src.app.core.database import Base


class OTP(Base):

    __tablename__ = "otps"

    id = Column(BigInteger, primary_key=True, index=True)

    email = Column(String(250), index=True, nullable=False)

    otp_code = Column(String(6), nullable=False)

    is_used = Column(Integer, default=0)

    expire_at = Column(TIMESTAMP, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
