from sqlalchemy import (
    Column,
    Integer,
    String
)

from src.app.models.base_entity import BaseEntity


class VehicleType(BaseEntity):

    __tablename__ = "vehicle_types"

    id = Column(
        Integer,
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

    description = Column(
        String(255)
    )
