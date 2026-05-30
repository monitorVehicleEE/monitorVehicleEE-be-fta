from sqlalchemy.orm import Session

from src.app.models.vehicle_types_model import VehicleType


class VehicleTypeRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(VehicleType).all()

    def get_by_id(self, type_id: int):
        return (
            self.db.query(VehicleType)
            .filter(VehicleType.id == type_id)
            .first()
        )

    def get_by_code(self, code: str):
        return (
            self.db.query(VehicleType)
            .filter(VehicleType.code == code)
            .first()
        )

    def create(self, vehicle_type: VehicleType):
        self.db.add(vehicle_type)
        self.db.commit()
        self.db.refresh(vehicle_type)

        return vehicle_type
