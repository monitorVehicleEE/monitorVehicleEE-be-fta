from src.app.models.vehicle_types_model import VehicleType


class VehicleTypeService:

    def __init__( self, vehicle_type_repository ):
        self.vehicle_type_repository = (
            vehicle_type_repository
        )

    def get_all(self):
        return (
            self.vehicle_type_repository
            .find_all()
        )

    def get_by_id(self, type_id: int):
        vehicle_type = (
            self.vehicle_type_repository
            .get_by_id(type_id)
        )

        if not vehicle_type:
            raise Exception("Vehicle type not found")

        return vehicle_type

    def get_by_code(self, code: str):
        vehicle_type = (
            self.vehicle_type_repository
            .get_by_code(code)
        )

        if not vehicle_type:
            raise Exception("Vehicle type not found")

        return vehicle_type

    def create( self, request ):

        vehicle_type = VehicleType(
            code=request.code,
            name=request.name,
            description=getattr(request, "description", None)
        )

        return (
            self.vehicle_type_repository
            .create(vehicle_type)
        )
