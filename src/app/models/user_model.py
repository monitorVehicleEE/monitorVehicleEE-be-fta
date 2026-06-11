
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    TIMESTAMP
)
from sqlalchemy.sql import func
from src.app.core.database import Base
from src.app.models.base_entity import BaseEntity

class User(BaseEntity):

    __tablename__ = "users"

    username = Column(
        String(250),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(250),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    fullname = Column(
        String(100)
    )

    avatar = Column(
        String(500)
    )

    type = Column(
        Integer,
        default=200,
        nullable=False
    )

    role = Column(
        Integer,
        default=0,
        nullable=False
    )

    def is_admin(self):
        return self.role == 1

    def update_avatar(self, avatar_url: str):
        self.avatar = avatar_url

