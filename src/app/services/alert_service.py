from datetime import datetime

from src.app.models.alert_model import Alert


class AlertService:

    def __init__(self, alert_repository):
        self.alert_repository = alert_repository

    def get_all(self, is_resolved: bool | None = None):
        return self.alert_repository.find_all(is_resolved=is_resolved)

    def get_recent(self, limit: int = 10, camera_id: int | None = None):
        return self.alert_repository.find_recent(
            limit=limit,
            camera_id=camera_id
        )

    def get_by_id(self, alert_id: int):
        alert = self.alert_repository.get_by_id(alert_id)

        if not alert:
            raise Exception("Alert not found")

        return alert

    def create(self, request):
        existing_alert = self.alert_repository.get_by_event_and_rule(
            request.vehicle_event_id,
            request.access_rule_id
        )

        if existing_alert:
            return existing_alert

        alert = Alert(
            vehicle_event_id=request.vehicle_event_id,
            access_rule_id=request.access_rule_id,
            plate=request.plate.strip().upper(),
            camera_id=request.camera_id,
            alert_type=request.alert_type,
            severity=request.severity,
            message=request.message,
            image_path=getattr(request, "image_path", None),
            plate_image_path=getattr(request, "plate_image_path", None)
        )

        return self.alert_repository.create(alert)

    def create_blacklist_alert(self, event, access_rule):
        existing_alert = self.alert_repository.get_by_event_and_rule(
            event.id,
            access_rule.id
        )

        if existing_alert:
            return existing_alert

        message = (
            f"Phát hiện xe trong danh sách đen {event.plate} "
            f"tại camera {event.camera_id}"
        )

        alert = Alert(
            vehicle_event_id=event.id,
            access_rule_id=access_rule.id,
            plate=event.plate,
            camera_id=event.camera_id,
            alert_type="BLACKLIST_DETECTED",
            severity="high",
            message=message,
            image_path=event.image_path,
            plate_image_path=event.plate_image_path
        )

        return self.alert_repository.create(alert)

    def resolve(self, alert_id: int, resolved_by: str | None = None):
        alert = self.get_by_id(alert_id)
        alert.is_resolved = True
        alert.resolved_by = resolved_by
        alert.resolved_at = datetime.now()

        return self.alert_repository.update(alert)

    def delete(self, alert_id: int):
        alert = self.get_by_id(alert_id)
        alert.soft_delete()

        return self.alert_repository.update(alert)
