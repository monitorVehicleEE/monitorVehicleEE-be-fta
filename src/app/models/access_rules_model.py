from sqlalchemy import (
    BigInteger,
    Column,
    String,
    TIMESTAMP
)

from src.app.models.base_entity import BaseEntity


class AccessRule(BaseEntity):

    __tablename__ = "access_rules"

    id = Column(
        BigInteger,
        primary_key=True
    )

    plate = Column(
        String(20)
    )

    rule_type = Column(
        String(20),
        nullable=False
    )

    description = Column(
        String(250)
    )

    valid_from = Column(
        TIMESTAMP
    )

    valid_to = Column(
        TIMESTAMP
    )
