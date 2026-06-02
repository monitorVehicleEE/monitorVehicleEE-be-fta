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

    def find_all(
        self,
        plate: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        query = (
            self.db.query(VehicleSession)
            .order_by(VehicleSession.in_time.desc())
        )

        if plate:
            query = query.filter(VehicleSession.plate == plate)

        if status:
            query = query.filter(VehicleSession.status == status)

        if skip:
            query = query.offset(skip)

        if limit:
            query = query.limit(limit)

        return query.all()

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
