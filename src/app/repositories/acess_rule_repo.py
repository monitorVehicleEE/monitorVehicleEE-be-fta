from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from src.app.models.access_rules_model import AccessRule


class AccessRuleRepository:

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _normalize_plate_value(plate: str):
        return (
            str(plate or "")
            .strip()
            .upper()
            .replace("-", "")
            .replace(".", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace("\r", "")
            .replace("\t", "")
        )

    @staticmethod
    def _normalize_plate_expr(column):
        normalized = func.upper(func.coalesce(column, ""))
        for char in ("-", ".", " ", "\n", "\r", "\t"):
            normalized = func.replace(normalized, char, "")
        return normalized

    def find_all(self):
        return (
            self.db.query(AccessRule)
            .filter(AccessRule.status != 10)
            .order_by(AccessRule.date_new.desc())
            .all()
        )

    def get_by_id(self, rule_id: int):
        return (
            self.db.query(AccessRule)
            .filter(AccessRule.id == rule_id)
            .filter(AccessRule.status != 10)
            .first()
        )

    def get_by_plate(self, plate: str):
        normalized_plate = self._normalize_plate_expr(AccessRule.plate)
        return (
            self.db.query(AccessRule)
            .filter(normalized_plate == self._normalize_plate_value(plate))
            .filter(AccessRule.status != 10)
            .order_by(AccessRule.date_new.desc())
            .all()
        )

    def find_active_by_plate(self, plate: str, at_time: datetime | None = None):
        target_time = at_time or datetime.now()
        normalized_plate = self._normalize_plate_expr(AccessRule.plate)

        return (
            self.db.query(AccessRule)
            .filter(normalized_plate == self._normalize_plate_value(plate))
            .filter(AccessRule.status == 1)
            .filter(
                or_(
                    AccessRule.valid_from.is_(None),
                    AccessRule.valid_from <= target_time
                )
            )
            .filter(
                or_(
                    AccessRule.valid_to.is_(None),
                    AccessRule.valid_to >= target_time
                )
            )
            .order_by(AccessRule.date_new.desc())
            .all()
        )

    def create(self, rule: AccessRule):
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)

        return rule

    def update(self, rule: AccessRule):
        self.db.commit()
        self.db.refresh(rule)

        return rule
