from datetime import datetime

from src.app.models.vehicle_event_model import VehicleEvent


class VehicleEventService:

    def __init__(self, vehicle_event_repository):
        self.vehicle_event_repository = vehicle_event_repository

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

    def create(self, request):
        plate = None

        if request.plate:
            plate = request.plate.strip().upper()

        event = VehicleEvent(
            camera_id=request.camera_id,
            plate=plate,
            event_type=request.event_type,
            vehicle_type=request.vehicle_type,
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
