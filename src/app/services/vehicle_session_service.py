from datetime import datetime

from src.app.models.vehicle_sessions_model import VehicleSession


class VehicleSessionService:

    def __init__(self, vehicle_session_repository):
        self.vehicle_session_repository = vehicle_session_repository

    def get_open_session(self, plate: str):
        return (
            self.vehicle_session_repository
            .get_open_session(plate.strip().upper())
        )

    def find_all(
        self,
        plate: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        normalized_plate = plate.strip().upper() if plate else None
        normalized_status = status.strip().upper() if status else None

        return self.vehicle_session_repository.find_all(
            plate=normalized_plate,
            status=normalized_status,
            skip=skip,
            limit=limit
        )

    def create(self, request):
        session = VehicleSession(
            plate=request.plate.strip().upper() if request.plate else None,
            in_event_id=getattr(request, "in_event_id", None),
            out_event_id=getattr(request, "out_event_id", None),
            in_camera_id=getattr(request, "in_camera_id", None),
            out_camera_id=getattr(request, "out_camera_id", None),
            in_time=getattr(request, "in_time", None) or datetime.now(),
            out_time=getattr(request, "out_time", None),
            duration_seconds=getattr(request, "duration_seconds", None),
            status=getattr(request, "status", None) or "OPEN"
        )

        return (
            self.vehicle_session_repository
            .create(session)
        )

    def create_open_session(
        self,
        plate: str,
        in_event_id=None,
        in_camera_id=None,
        in_time=None
    ):
        session = VehicleSession(
            plate=plate.strip().upper(),
            in_event_id=in_event_id,
            in_camera_id=in_camera_id,
            in_time=in_time or datetime.now(),
            status="OPEN"
        )

        return (
            self.vehicle_session_repository
            .create(session)
        )

    def close_session(
        self,
        plate: str,
        out_event_id=None,
        out_camera_id=None,
        out_time=None
    ):
        session = self.get_open_session(plate)

        if not session:
            raise Exception("Open vehicle session not found")

        session.out_event_id = out_event_id
        session.out_camera_id = out_camera_id
        session.out_time = out_time or datetime.now()
        session.status = "CLOSED"

        if session.in_time and session.out_time:
            duration = session.out_time - session.in_time
            session.duration_seconds = int(duration.total_seconds())

        return (
            self.vehicle_session_repository
            .update(session)
        )
