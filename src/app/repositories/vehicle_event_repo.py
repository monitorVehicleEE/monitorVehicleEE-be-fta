from sqlalchemy.orm import Session

from src.app.models.vehicle_event_model import VehicleEvent


class VehicleEventRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, event: VehicleEvent):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    def find_by_plate(self, plate: str):
        return (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.plate == plate)
            .all()
        )

    def find_latest_by_plate(self, plate: str):
        return (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.plate == plate)
            .order_by(
                VehicleEvent.event_time.desc()
            )
            .first()
        )
