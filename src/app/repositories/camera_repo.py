from sqlalchemy.orm import Session
from sqlalchemy import func

from src.app.models.camera_model import Camera


class CameraRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Camera).all()

    def get_by_id(self, camera_id: int):
        return (
            self.db.query(Camera)
            .filter(Camera.id == camera_id)
            .first()
        )

    def get_by_code(self, code: str):
        return (
            self.db.query(Camera)
            .filter(Camera.code == code)
            .first()
        )

    def get_max_id(self):
        return self.db.query(func.max(Camera.id)).scalar() or 0

    def create(self, camera: Camera):
        self.db.add(camera)
        self.db.commit()
        self.db.refresh(camera)

        return camera

    def update(self, camera: Camera):
        self.db.commit()
        self.db.refresh(camera)

        return camera
