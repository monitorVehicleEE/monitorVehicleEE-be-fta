import os
from datetime import datetime

from src.app.models.vehicle_event_model import VehicleEvent

EVENT_DEDUPE_SECONDS = int(os.getenv("VEHICLE_EVENT_DEDUPE_SECONDS", "30"))
NO_PLATE_EVENT_DEDUPE_SECONDS = int(
    os.getenv("VEHICLE_EVENT_NO_PLATE_DEDUPE_SECONDS", "5")
)


class VehicleEventService:

    vehicle_type_aliases = {
        "motorbike": 1,
        "motorcycle": 1,
        "xm": 1,
        "car": 2,
        "oto": 2,
        "truck": 3,
        "xt": 3,
        "xe-tai": 3,
        "container": 4,
        "xctn": 4,
        "xe-container": 4,
    }

    def __init__(self, vehicle_event_repository):
        self.vehicle_event_repository = vehicle_event_repository

    def _parse_vehicle_type_id(self, vehicle_type: str | None):
        if not vehicle_type:
            return None

        normalized = vehicle_type.strip().lower()
        if normalized.isdigit():
            return int(normalized)

        return self.vehicle_type_aliases.get(normalized)

    def find_by_plate(self, plate: str):
        return (
            self.vehicle_event_repository
            .find_by_plate(plate.strip().upper())
        )

    def find_latest_by_plate(self, plate: str):
        return (
            self.vehicle_event_repository
            .find_latest_by_plate(plate.strip().upper())
        )

    def find_history(
        self,
        camera_id: int | None = None,
        vehicle_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        vehicle_type_id = self._parse_vehicle_type_id(vehicle_type)
        return self.vehicle_event_repository.find_history(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )

    def find_pending(self, limit: int = 20):
        return self.vehicle_event_repository.find_pending(limit)

    def live_feed(self):
        return {
            "approved": self.vehicle_event_repository.find_recent_approved(10),
            "pending": self.vehicle_event_repository.find_pending(20)
        }

    def update(self, event_id: int, request, default_status: str | None = None):
        event = self.vehicle_event_repository.get_by_id(event_id)

        if not event:
            raise Exception("Vehicle event not found")

        fields_set = getattr(request, "model_fields_set", set())

        if "plate" in fields_set:
            plate = getattr(request, "plate", None)
            event.plate = plate.strip().upper() if plate else None

        if "vehicle_type_id" in fields_set:
            event.vehicle_type_id = getattr(request, "vehicle_type_id", None)

        status = getattr(request, "status", None) or default_status
        if status:
            event.status = status

        return self.vehicle_event_repository.update(event)

    def approve(self, event_id: int, request):
        return self.update(
            event_id,
            request,
            default_status="MANUAL_APPROVED"
        )

    def reject(self, event_id: int, request):
        event = self.vehicle_event_repository.get_by_id(event_id)

        if not event:
            raise Exception("Vehicle event not found")

        return self.vehicle_event_repository.delete(event)

    def create(self, request):
        plate = None

        if request.plate:
            plate = request.plate.strip().upper()

        duplicate = self.vehicle_event_repository.find_recent_duplicate(
            camera_id=request.camera_id,
            event_type=request.event_type,
            plate=plate,
            seconds=(
                EVENT_DEDUPE_SECONDS
                if plate
                else NO_PLATE_EVENT_DEDUPE_SECONDS
            )
        )

        if duplicate:
            return duplicate

        event = VehicleEvent(
            camera_id=request.camera_id,
            plate=plate,
            event_type=request.event_type,
            vehicle_type_id=request.vehicle_type_id,
            vehicle_confidence=request.vehicle_confidence,
            plate_confidence=request.plate_confidence,
            image_path=request.image_path,
            plate_image_path=request.plate_image_path,
            bbox=request.bbox,
            status=request.status or "PENDING",
            event_time=getattr(request, "event_time", None) or datetime.now()
        )

        return (
            self.vehicle_event_repository
            .create(event)
        )
