from sqlalchemy import func
from sqlalchemy.orm import Session

from src.app.models.vehicle_model import Vehicle


class VehicleRepository:

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
        return self.db.query(Vehicle).all()

    def get_by_id(self, vehicle_id: int):
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.id == vehicle_id)
            .first()
        )

    def get_by_plate(self, plate: str):
        normalized_plate = self._normalize_plate_expr(Vehicle.plate)
        return (
            self.db.query(Vehicle)
            .filter(normalized_plate == self._normalize_plate_value(plate))
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
