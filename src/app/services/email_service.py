import smtplib
from email.mime.text import MIMEText


class EmailService:

    def send_otp_email(self, to_email: str, otp_code: str):

        msg = MIMEText(f"Your OTP code is: {otp_code}")
        msg["Subject"] = "VehicleOps OTP Verification"
        msg["From"] = "minhait81@gmail.com"
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("minhait81@gmail.com", "zprm zukw pudx zimj")
        server.send_message(msg)
        server.quit()