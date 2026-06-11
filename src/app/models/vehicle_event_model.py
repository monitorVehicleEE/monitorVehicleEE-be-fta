from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    TIMESTAMP
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from src.app.core.database import Base


class VehicleEvent(Base):

    __tablename__ = "vehicle_events"

    id = Column(
        BigInteger,
        primary_key=True
    )

    camera_id = Column(
        BigInteger,
        ForeignKey("cameras.id"),
        nullable=False
    )

    plate = Column(
        String(20)
    )

    vehicle_type_id = Column(
        Integer,
        ForeignKey("vehicle_types.id")
    )

    event_type = Column(
        String(20),
        nullable=False
    )

    vehicle_confidence = Column(
        Numeric(5, 2)
    )

    plate_confidence = Column(
        Numeric(5, 2)
    )

    image_path = Column(
        String(500)
    )

    plate_image_path = Column(
        String(500)
    )

    bbox = Column(
        JSONB
    )

    status = Column(
        Integer,
        server_default="0",
        nullable=False
    )

    event_time = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    date_new = Column(
        TIMESTAMP,
        server_default=func.now()
    )
