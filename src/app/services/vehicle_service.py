from src.app.models.vehicle_model import Vehicle


class VehicleService:

    def __init__(
        self,
        vehicle_repository,
        vehicle_type_repository=None
    ):
        self.vehicle_repository = vehicle_repository
        self.vehicle_type_repository = vehicle_type_repository

    @staticmethod
    def _normalize_plate(plate: str):
        return plate.strip().upper()

    @staticmethod
    def _normalize_text(value: str | None):
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None

    def _ensure_vehicle_type_exists(self, vehicle_type_id: int | None):
        if vehicle_type_id is None or not self.vehicle_type_repository:
            return

        vehicle_type = self.vehicle_type_repository.get_by_id(vehicle_type_id)
        if not vehicle_type:
            raise Exception("Vehicle type not found")

    def _ensure_plate_available(self, plate: str, vehicle_id: int | None = None):
        existing_vehicle = self.vehicle_repository.get_by_plate(plate)
        if existing_vehicle and existing_vehicle.id != vehicle_id:
            raise Exception("Vehicle already exists")

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
            .get_by_plate(self._normalize_plate(plate))
        )

        if not vehicle:
            raise Exception("Vehicle not found")

        return vehicle

    def create(self, request):
        plate = self._normalize_plate(request.plate)
        self._ensure_plate_available(plate)
        self._ensure_vehicle_type_exists(request.vehicle_type_id)

        vehicle = Vehicle(
            plate=plate,
            owner_name=self._normalize_text(getattr(request, "owner_name", None)),
            owner_phone=self._normalize_text(getattr(request, "owner_phone", None)),
            owner_cccd=self._normalize_text(getattr(request, "owner_cccd", None)),
            owner_address=self._normalize_text(getattr(request, "owner_address", None)),
            vehicle_type_id=request.vehicle_type_id,
            is_internal=request.is_internal
        )

        return (
            self.vehicle_repository
            .create(vehicle)
        )

    def update(self, vehicle_id: int, request):
        vehicle = self.get_by_id(vehicle_id)

        if getattr(request, "plate", None):
            plate = self._normalize_plate(request.plate)
            self._ensure_plate_available(plate, vehicle_id=vehicle.id)
            vehicle.plate = plate

        if getattr(request, "is_internal", None) is not None:
            vehicle.is_internal = request.is_internal

        if "owner_name" in getattr(request, "model_fields_set", set()):
            vehicle.owner_name = self._normalize_text(getattr(request, "owner_name", None))

        if "owner_phone" in getattr(request, "model_fields_set", set()):
            vehicle.owner_phone = self._normalize_text(getattr(request, "owner_phone", None))

        if "owner_cccd" in getattr(request, "model_fields_set", set()):
            vehicle.owner_cccd = self._normalize_text(getattr(request, "owner_cccd", None))

        if "owner_address" in getattr(request, "model_fields_set", set()):
            vehicle.owner_address = self._normalize_text(getattr(request, "owner_address", None))

        if (
            getattr(request, "vehicle_type_id", None) is not None
            and self.vehicle_type_repository
        ):
            self._ensure_vehicle_type_exists(request.vehicle_type_id)
            vehicle.vehicle_type_id = request.vehicle_type_id

        return (
            self.vehicle_repository
            .update(vehicle)
        )
