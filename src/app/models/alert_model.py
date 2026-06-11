from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    String,
    TIMESTAMP
)

from src.app.models.base_entity import BaseEntity


class Alert(BaseEntity):

    __tablename__ = "alerts"

    id = Column(
        BigInteger,
        primary_key=True
    )

    vehicle_event_id = Column(
        BigInteger,
        ForeignKey("vehicle_events.id"),
        nullable=False
    )

    access_rule_id = Column(
        BigInteger,
        ForeignKey("access_rules.id")
    )

    plate = Column(
        String(20),
        nullable=False
    )

    camera_id = Column(
        BigInteger,
        ForeignKey("cameras.id"),
        nullable=False
    )

    alert_type = Column(
        String(50),
        nullable=False
    )

    severity = Column(
        String(20),
        nullable=False,
        default="high"
    )

    message = Column(
        String(500),
        nullable=False
    )

    image_path = Column(
        String(500)
    )

    plate_image_path = Column(
        String(500)
    )

    is_resolved = Column(
        Boolean,
        default=False,
        nullable=False
    )

    resolved_by = Column(
        String(100)
    )

    resolved_at = Column(
        TIMESTAMP
    )

    @property
    def timestamp(self):
        return self.date_new

    @property
    def vehicle_id(self):
        return self.vehicle_event_id
