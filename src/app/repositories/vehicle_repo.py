from sqlalchemy.orm import Session

from src.app.models.vehicle_model import Vehicle


class VehicleRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Vehicle).all()

    def get_by_id(self, vehicle_id: int):
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.id == vehicle_id)
            .first()
        )

    def get_by_plate(self, plate: str):
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.plate == plate)
            .first()
        )

    def create(self, vehicle: Vehicle):
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle

    def update(self, vehicle: Vehicle):
        self.db.commit()
        self.db.refresh(vehicle)

        return vehicle
