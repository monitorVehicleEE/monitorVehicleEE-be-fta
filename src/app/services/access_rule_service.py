from src.app.models.access_rules_model import AccessRule


class AccessRuleService:

    def __init__(
        self,
        access_rule_repository,
        vehicle_repository
    ):
        self.access_rule_repository = access_rule_repository
        self.vehicle_repository = vehicle_repository

    @staticmethod
    def _normalize_plate(plate: str):
        return plate.strip().upper()

    @staticmethod
    def _normalize_text(value: str | None):
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None

    @staticmethod
    def _validate_time_range(valid_from, valid_to):
        if (
            valid_from is not None
            and valid_to is not None
            and valid_from > valid_to
        ):
            raise Exception("valid_from must be before valid_to")

    def _get_vehicle_by_plate(self, plate: str):
        vehicle = self.vehicle_repository.get_by_plate(plate)

        if not vehicle:
            raise Exception("Vehicle not found")

        return vehicle

    def get_all(self):
        return (
            self.access_rule_repository
            .find_all()
        )

    def get_by_id(self, rule_id: int):
        rule = (
            self.access_rule_repository
            .get_by_id(rule_id)
        )

        if not rule:
            raise Exception("Access rule not found")

        return rule

    def get_by_plate(self, plate: str):
        return (
            self.access_rule_repository
            .get_by_plate(self._normalize_plate(plate))
        )

    def find_active_by_plate(self, plate: str, at_time=None):
        return (
            self.access_rule_repository
            .find_active_by_plate(
                self._normalize_plate(plate),
                at_time=at_time
            )
        )

    def create(self, request):
        plate = self._normalize_plate(request.plate)
        vehicle = self._get_vehicle_by_plate(plate)
        self._validate_time_range(request.valid_from, request.valid_to)

        rule = AccessRule(
            plate=vehicle.plate,
            rule_type=request.rule_type,
            description=self._normalize_text(request.description),
            valid_from=getattr(request, "valid_from", None),
            valid_to=getattr(request, "valid_to", None)
        )

        return (
            self.access_rule_repository
            .create(rule)
        )

    def update(self, rule_id: int, request):
        rule = self.get_by_id(rule_id)
        fields_set = getattr(request, "model_fields_set", set())

        if "plate" in fields_set and request.plate is not None:
            plate = self._normalize_plate(request.plate)
            vehicle = self._get_vehicle_by_plate(plate)
            rule.plate = vehicle.plate

        if "rule_type" in fields_set and request.rule_type is not None:
            rule.rule_type = request.rule_type

        if "description" in fields_set:
            rule.description = self._normalize_text(request.description)

        if "valid_from" in fields_set:
            rule.valid_from = request.valid_from

        if "valid_to" in fields_set:
            rule.valid_to = request.valid_to

        if "status" in fields_set and request.status is not None:
            rule.status = request.status

        self._validate_time_range(rule.valid_from, rule.valid_to)

        return self.access_rule_repository.update(rule)

    def delete(self, rule_id: int):
        rule = self.get_by_id(rule_id)
        rule.soft_delete()

        return self.access_rule_repository.update(rule)
