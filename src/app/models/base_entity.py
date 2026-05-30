from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    TIMESTAMP
)

from sqlalchemy.sql import func

from src.app.core.database import Base


class BaseEntity(Base):

    __abstract__ = True

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    status = Column(
        Integer,
        default=1,
        nullable=False
    )

    date_new = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    date_mod = Column(
        TIMESTAMP(timezone=True),
        onupdate=func.now()
    )

    def soft_delete(self):
        self.status = 10

    def is_active(self):
        return self.status == 1


