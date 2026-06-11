import os
from datetime import datetime

from src.app.models.vehicle_event_model import VehicleEvent
from src.app.repositories.acess_rule_repo import AccessRuleRepository
from src.app.repositories.alert_repo import AlertRepository
from src.app.repositories.vehicle_session_repo import VehicleSessionRepository
from src.app.schemas.access_rule_schema import RULE_BLACKLIST
from src.app.services.alert_service import AlertService
from src.app.services.vehicle_session_service import VehicleSessionService

EVENT_DEDUPE_SECONDS = int(os.getenv("VEHICLE_EVENT_DEDUPE_SECONDS", "30"))
NO_PLATE_EVENT_DEDUPE_SECONDS = int(
    os.getenv("VEHICLE_EVENT_NO_PLATE_DEDUPE_SECONDS", "5")
)


def is_suspicious_plate_format(plate: str | None):
    if not plate or "-" not in plate:
        return False

    prefix, suffix = plate.strip().upper().split("-", 1)
    normalized_suffix = (
        suffix
        .replace(".", "")
        .replace(" ", "")
        .replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
    )

    return len(prefix) == 4 and len(normalized_suffix) <= 4


class VehicleEventService:

    def __init__(self, vehicle_event_repository):
        self.vehicle_event_repository = vehicle_event_repository
        self.vehicle_session_service = VehicleSessionService(
            VehicleSessionRepository(vehicle_event_repository.db)
        )
        self.access_rule_repository = AccessRuleRepository(
            vehicle_event_repository.db
        )
        self.alert_service = AlertService(
            AlertRepository(vehicle_event_repository.db)
        )

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
        vehicle_type_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        return self.vehicle_event_repository.find_history(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )

    def find_history_page(
        self,
        camera_id: int | None = None,
        vehicle_type_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int | None = None
    ):
        items = self.vehicle_event_repository.find_history(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        total = self.vehicle_event_repository.count_history(
            camera_id=camera_id,
            vehicle_type_id=vehicle_type_id,
            start_date=start_date,
            end_date=end_date
        )

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    def find_pending(
        self,
        limit: int = 20,
        camera_id: int | None = None
    ):
        return self.vehicle_event_repository.find_pending(
            limit=limit,
            camera_id=camera_id
        )

    def live_feed(self, camera_id: int | None = None):
        return {
            "approved": self.vehicle_event_repository.find_recent_approved(
                limit=10,
                camera_id=camera_id
            ),
            "pending": self.vehicle_event_repository.find_pending(
                limit=20,
                camera_id=camera_id
            ),
            "alerts": self.alert_service.get_recent(
                limit=10,
                camera_id=camera_id
            )
        }

    def _create_access_rule_alerts(self, event: VehicleEvent):
        if not event or not event.plate:
            return []

        access_rules = self.access_rule_repository.find_active_by_plate(
            event.plate,
            at_time=event.event_time
        )

        alerts = []

        for access_rule in access_rules:
            if access_rule.rule_type != RULE_BLACKLIST:
                continue

            alerts.append(
                self.alert_service.create_blacklist_alert(
                    event,
                    access_rule
                )
            )

        return alerts

    def _sync_vehicle_session(self, event: VehicleEvent):
        if (
            not event
            or not event.plate
            or event.status not in {1, 2}
        ):
            return None

        event_type = (event.event_type or "").strip().upper()

        if event_type == "IN":
            open_session = self.vehicle_session_service.get_open_session(
                event.plate
            )

            if open_session:
                return open_session

            return self.vehicle_session_service.create_open_session(
                plate=event.plate,
                in_event_id=event.id,
                in_camera_id=event.camera_id,
                in_time=event.event_time
            )

        if event_type == "OUT":
            open_session = self.vehicle_session_service.get_open_session(
                event.plate
            )

            if not open_session:
                return None

            return self.vehicle_session_service.close_session(
                plate=event.plate,
                out_event_id=event.id,
                out_camera_id=event.camera_id,
                out_time=event.event_time
            )

        return None

    def update(self, event_id: int, request, default_status: int | None = None):
        event = self.vehicle_event_repository.get_by_id(event_id)

        if not event:
            raise Exception("Vehicle event not found")

        fields_set = getattr(request, "model_fields_set", set())

        if "plate" in fields_set:
            plate = getattr(request, "plate", None)
            event.plate = plate.strip().upper() if plate else None

        if "vehicle_type_id" in fields_set:
            event.vehicle_type_id = getattr(request, "vehicle_type_id", None)

        request_status = getattr(request, "status", None)
        status = request_status if request_status is not None else default_status
        if status is not None:
            event.status = status

        updated_event = self.vehicle_event_repository.update(event)
        self._create_access_rule_alerts(updated_event)
        self._sync_vehicle_session(updated_event)

        return updated_event

    def approve(self, event_id: int, request):
        return self.update(
            event_id,
            request,
            default_status=2
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
            self._create_access_rule_alerts(duplicate)
            return duplicate

        status = request.status if request.status is not None else 0
        if is_suspicious_plate_format(plate):
            status = 0

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
            status=status,
            event_time=getattr(request, "event_time", None) or datetime.now()
        )

        created_event = self.vehicle_event_repository.create(event)
        self._create_access_rule_alerts(created_event)
        self._sync_vehicle_session(created_event)

        return created_event

