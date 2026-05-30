from sqlalchemy.orm import Session

from src.app.models.access_rules_model import AccessRule


class AccessRuleRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(AccessRule).all()

    def get_by_id(self, rule_id: int):
        return (
            self.db.query(AccessRule)
            .filter(AccessRule.id == rule_id)
            .first()
        )

    def get_by_plate(self, plate: str):
        return (
            self.db.query(AccessRule)
            .filter(
                AccessRule.plate == plate
            )
            .all()
        )

    def create(self, rule: AccessRule):
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)

        return rule
