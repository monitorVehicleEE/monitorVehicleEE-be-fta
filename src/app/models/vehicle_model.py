from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
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

    owner_name = Column(
        String(100)
    )

    owner_phone = Column(
        String(20)
    )

    owner_cccd = Column(
        String(20)
    )

    owner_address = Column(
        String(255)
    )

    vehicle_type_id = Column(
        Integer,
        ForeignKey("vehicle_types.id")
    )

    is_internal = Column(
        Boolean,
        default=False
    )

    @property
    def vehicle_type(self):
        return self.vehicle_type_id
