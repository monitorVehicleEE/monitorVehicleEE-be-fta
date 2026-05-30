import random
from datetime import datetime, timedelta, timezone


class OTPService:

    OTP_EXPIRE_MINUTES = 5
    VIETNAM_TIMEZONE = timezone(timedelta(hours=7))

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def now(self):
        return datetime.now(self.VIETNAM_TIMEZONE).replace(tzinfo=None)

    def get_expire_time(self):
        return self.now() + timedelta(minutes=self.OTP_EXPIRE_MINUTES)

    def verify_otp(self, otp_obj, input_code: str):

        if otp_obj.is_used == 1:
            return False

        if otp_obj.otp_code != input_code:
            return False

        if otp_obj.expire_at < self.now():
            return False

        return True
