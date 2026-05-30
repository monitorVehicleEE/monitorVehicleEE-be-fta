from sqlalchemy.orm import Session

from src.app.models.vehicle_sessions_model import VehicleSession


class VehicleSessionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, session: VehicleSession):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_open_session( self, plate: str):
        return (
            self.db.query(VehicleSession)
            .filter(
                VehicleSession.plate == plate,
                VehicleSession.status == "OPEN"
            )
            .first()
        )

    def update(self, session: VehicleSession):
        self.db.commit()
        self.db.refresh(session)

        return session
