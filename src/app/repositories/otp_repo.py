from sqlalchemy.orm import Session

from src.app.models.otp_model import OTP


class OTPRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, otp: OTP):

        self.db.add(otp)

        self.db.commit()

        self.db.refresh(otp)

        return otp

    def get_latest_by_email(self, email: str):

        return (
            self.db.query(OTP)
            .filter(OTP.email == email)
            .order_by(OTP.id.desc())
            .first()
        )

    def update(self, otp: OTP):

        self.db.commit()

        self.db.refresh(otp)

        return otp
