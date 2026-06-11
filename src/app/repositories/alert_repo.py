from sqlalchemy.orm import Session

from src.app.models.alert_model import Alert


class AlertRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self, is_resolved: bool | None = None):
        query = (
            self.db.query(Alert)
            .filter(Alert.status != 10)
        )

        if is_resolved is not None:
            query = query.filter(Alert.is_resolved == is_resolved)

        return (
            query
            .order_by(Alert.date_new.desc())
            .all()
        )

    def find_recent(self, limit: int = 10, camera_id: int | None = None):
        query = (
            self.db.query(Alert)
            .filter(Alert.status != 10)
            .filter(Alert.is_resolved.is_(False))
        )

        if camera_id is not None:
            query = query.filter(Alert.camera_id == camera_id)

        return (
            query
            .order_by(Alert.date_new.desc())
            .limit(limit)
            .all()
        )

    def get_by_id(self, alert_id: int):
        return (
            self.db.query(Alert)
            .filter(Alert.id == alert_id)
            .filter(Alert.status != 10)
            .first()
        )

    def get_by_event_and_rule(
        self,
        vehicle_event_id: int,
        access_rule_id: int | None
    ):
        query = (
            self.db.query(Alert)
            .filter(Alert.vehicle_event_id == vehicle_event_id)
            .filter(Alert.status != 10)
        )

        if access_rule_id is None:
            query = query.filter(Alert.access_rule_id.is_(None))
        else:
            query = query.filter(Alert.access_rule_id == access_rule_id)

        return query.first()

    def create(self, alert: Alert):
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)

        return alert

    def update(self, alert: Alert):
        self.db.commit()
        self.db.refresh(alert)

        return alert
