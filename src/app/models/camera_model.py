from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String
)

from src.app.models.base_entity import BaseEntity


class Camera(BaseEntity):

    __tablename__ = "cameras"

    id = Column(
        BigInteger,
        primary_key=True
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    location = Column(
        String(250)
    )

    camera_role = Column(
        Integer,
        nullable=False
    )

    source_type = Column(
        String(20),
        nullable=False
    )

    source_path = Column(
        String(500),
        nullable=False
    )
