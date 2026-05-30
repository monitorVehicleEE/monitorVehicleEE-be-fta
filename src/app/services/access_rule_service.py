from src.app.models.access_rules_model import AccessRule


class AccessRuleService:

    def __init__(
        self,
        access_rule_repository,
        vehicle_repository
    ):
        self.access_rule_repository = access_rule_repository
        self.vehicle_repository = vehicle_repository

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
            .get_by_plate(plate.strip().upper())
        )

    def create(self, request):
        plate = request.plate.strip().upper()

        vehicle = (
            self.vehicle_repository
            .get_by_plate(plate)
        )

        if not vehicle:
            raise Exception("Vehicle not found")

        rule = AccessRule(
            plate=vehicle.plate,
            rule_type=request.rule_type,
            description=request.description,
            valid_from=getattr(request, "valid_from", None),
            valid_to=getattr(request, "valid_to", None)
        )

        return (
            self.access_rule_repository
            .create(rule)
        )
