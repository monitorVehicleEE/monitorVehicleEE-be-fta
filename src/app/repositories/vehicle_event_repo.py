from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.app.models.vehicle_event_model import VehicleEvent


class VehicleEventRepository:

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

    def create(self, event: VehicleEvent):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    def update(self, event: VehicleEvent):
        self.db.commit()
        self.db.refresh(event)

        return event

    def delete(self, event: VehicleEvent):
        event_id = event.id
        self.db.delete(event)
        self.db.commit()

        return {
            "id": event_id,
            "status": "DELETED"
        }

    def get_by_id(self, event_id: int):
        return (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.id == event_id)
            .first()
        )

    def find_history(
        self,
        camera_id: int | None = None,
        vehicle_type_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        query = self._history_query(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date
        ).order_by(VehicleEvent.event_time.desc())

        if skip:
            query = query.offset(skip)

        if limit:
            query = query.limit(limit)

        return query.all()

    def count_history(
        self,
        camera_id: int | None = None,
        vehicle_type_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ):
        return self._history_query(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date
        ).count()

    def _history_query(
        self,
        camera_id: int | None = None,
        vehicle_type_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ):
        query = (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.status != 0)
        )

        if camera_id is not None:
            query = query.filter(VehicleEvent.camera_id == camera_id)

        if vehicle_type_id is not None:
            query = query.filter(VehicleEvent.vehicle_type_id == vehicle_type_id)

        if start_date is not None:
            query = query.filter(VehicleEvent.event_time >= start_date)

        if end_date is not None:
            query = query.filter(VehicleEvent.event_time <= end_date)

        return query

    def find_pending(
        self,
        limit: int = 20,
        camera_id: int | None = None
    ):
        query = (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.status == 0)
        )

        if camera_id is not None:
            query = query.filter(VehicleEvent.camera_id == camera_id)

        return (
            query
            .order_by(VehicleEvent.event_time.desc())
            .limit(limit)
            .all()
        )

    def find_recent_approved(
        self,
        limit: int = 10,
        camera_id: int | None = None
    ):
        query = (
            self.db.query(VehicleEvent)
            .filter(
                VehicleEvent.status.in_([1, 2])
            )
        )

        if camera_id is not None:
            query = query.filter(VehicleEvent.camera_id == camera_id)

        return (
            query
            .order_by(VehicleEvent.event_time.desc())
            .limit(limit)
            .all()
        )

    def find_recent_duplicate(
        self,
        camera_id: int,
        event_type: str,
        plate: str | None,
        seconds: int = 30
    ):
        cutoff = datetime.now() - timedelta(seconds=seconds)

        query = (
            self.db.query(VehicleEvent)
            .filter(VehicleEvent.camera_id == camera_id)
            .filter(VehicleEvent.event_type == event_type)
            .filter(VehicleEvent.event_time >= cutoff)
        )

        if plate:
            query = query.filter(
                self._normalize_plate_expr(VehicleEvent.plate)
                == self._normalize_plate_value(plate)
            )
        else:
            query = query.filter(VehicleEvent.plate.is_(None))

        return (
            query
            .order_by(VehicleEvent.event_time.desc())
            .first()
        )

    def find_by_plate(self, plate: str):
        normalized_plate = self._normalize_plate_expr(VehicleEvent.plate)
        return (
            self.db.query(VehicleEvent)
            .filter(normalized_plate == self._normalize_plate_value(plate))
            .order_by(VehicleEvent.event_time.desc())
            .all()
        )

    def find_latest_by_plate(self, plate: str):
        normalized_plate = self._normalize_plate_expr(VehicleEvent.plate)
        return (
            self.db.query(VehicleEvent)
            .filter(normalized_plate == self._normalize_plate_value(plate))
            .order_by(
                VehicleEvent.event_time.desc()
            )
            .first()
        )
