from src.app.models.vehicle_model import Vehicle


class VehicleService:

    def __init__(
        self,
        vehicle_repository,
        vehicle_type_repository=None
    ):
        self.vehicle_repository = vehicle_repository
        self.vehicle_type_repository = vehicle_type_repository

    def get_all(self):
        return (
            self.vehicle_repository
            .find_all()
        )

    def get_by_id(self, vehicle_id: int):
        vehicle = (
            self.vehicle_repository
            .get_by_id(vehicle_id)
        )

        if not vehicle:
            raise Exception("Vehicle not found")

        return vehicle

    def get_by_plate(self, plate: str):
        vehicle = (
            self.vehicle_repository
            .get_by_plate(plate.strip().upper())
        )

        if not vehicle:
            raise Exception("Vehicle not found")

        return vehicle

    def create(self, request):
        plate = request.plate.strip().upper()

        existing_vehicle = (
            self.vehicle_repository
            .get_by_plate(plate)
        )

        if existing_vehicle:
            raise Exception("Vehicle already exists")

        vehicle_type_code = None

        if request.vehicle_type and self.vehicle_type_repository:
            vehicle_type = (
                self.vehicle_type_repository
                .get_by_code(request.vehicle_type)
            )

            if not vehicle_type:
                raise Exception("Vehicle type not found")

            vehicle_type_code = vehicle_type.code

        vehicle = Vehicle(
            plate=plate,
            type=vehicle_type_code,
            is_internal=request.is_internal
        )

        return (
            self.vehicle_repository
            .create(vehicle)
        )

    def update(self, vehicle_id: int, request):
        vehicle = self.get_by_id(vehicle_id)

        if getattr(request, "plate", None):
            vehicle.plate = request.plate.strip().upper()

        if getattr(request, "is_internal", None) is not None:
            vehicle.is_internal = request.is_internal

        if getattr(request, "vehicle_type", None) and self.vehicle_type_repository:
            vehicle_type = (
                self.vehicle_type_repository
                .get_by_code(request.vehicle_type)
            )

            if not vehicle_type:
                raise Exception("Vehicle type not found")

            vehicle.type = vehicle_type.code

        return (
            self.vehicle_repository
            .update(vehicle)
        )
