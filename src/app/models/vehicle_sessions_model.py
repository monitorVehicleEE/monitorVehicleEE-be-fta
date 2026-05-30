from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey
)

from src.app.models.base_entity import BaseEntity


class VehicleSession(BaseEntity):

    __tablename__ = "vehicle_sessions"

    id = Column(
        BigInteger,
        primary_key=True
    )

    vehicle_id = Column(
        BigInteger,
        ForeignKey("vehicles.id")
    )

    plate = Column(
        String(20)
    )

    in_event_id = Column(
        BigInteger,
        ForeignKey("vehicle_events.id")
    )

    out_event_id = Column(
        BigInteger,
        ForeignKey("vehicle_events.id")
    )

    in_camera_id = Column(
        BigInteger,
        ForeignKey("cameras.id")
    )

    out_camera_id = Column(
        BigInteger,
        ForeignKey("cameras.id")
    )

    in_time = Column(
        TIMESTAMP,
        nullable=False
    )

    out_time = Column(
        TIMESTAMP
    )

    duration_seconds = Column(
        Integer
    )

    status = Column(
        String(20)
    )
