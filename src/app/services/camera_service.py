from src.app.models.camera_model import Camera


class CameraService:

    def __init__( self, camera_repository ):
        self.camera_repository = (
            camera_repository
        )

    def get_all(self):
        return (
            self.camera_repository
            .find_all()
        )

    def get_by_id(self, camera_id: int):
        camera = (
            self.camera_repository
            .get_by_id(camera_id)
        )

        if not camera:
            raise Exception("Camera not found")

        return camera

    def get_by_code(self, code: str):
        camera = (
            self.camera_repository
            .get_by_code(code)
        )

        if not camera:
            raise Exception("Camera not found")

        return camera

    def create(
        self,
        request
    ):
        code = self._resolve_code(request.code)

        camera = Camera(
            code=code,
            name=request.name,
            location=request.location,
            camera_role=request.camera_role,
            source_type=request.source_type,
            source_path=request.source_path
        )

        return (
            self.camera_repository
            .create(camera)
        )

    def update(self, camera_id: int, request):
        camera = self.get_by_id(camera_id)

        if request.code is not None:
            code = request.code.strip()
            if not code:
                raise Exception("Camera code cannot be empty")

            existing = self.camera_repository.get_by_code(code)
            if existing and existing.id != camera.id:
                raise Exception("Camera code already exists")

            camera.code = code

        if request.name is not None:
            camera.name = request.name

        if request.location is not None:
            camera.location = request.location

        if request.camera_role is not None:
            camera.camera_role = request.camera_role

        if request.source_type is not None:
            camera.source_type = request.source_type

        if request.source_path is not None:
            camera.source_path = request.source_path

        if request.status is not None:
            camera.status = request.status

        return (
            self.camera_repository
            .update(camera)
        )

    def _resolve_code(self, request_code):
        if request_code is not None and request_code.strip():
            code = request_code.strip()
            if self.camera_repository.get_by_code(code):
                raise Exception("Camera code already exists")
            return code

        next_id = self.camera_repository.get_max_id() + 1
        code = f"CAM{next_id:04d}"

        while self.camera_repository.get_by_code(code):
            next_id += 1
            code = f"CAM{next_id:04d}"

        return code
