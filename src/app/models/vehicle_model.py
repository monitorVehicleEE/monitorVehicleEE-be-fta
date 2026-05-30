from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    String
)

from src.app.models.base_entity import BaseEntity


class Vehicle(BaseEntity):

    __tablename__ = "vehicles"

    id = Column(
        BigInteger,
        primary_key=True
    )

    plate = Column(
        String(20),
        unique=True,
        nullable=False
    )

    type = Column(
        String(50)
    )

    is_internal = Column(
        Boolean,
        default=False
    )

    @property
    def vehicle_type(self):
        return self.type

