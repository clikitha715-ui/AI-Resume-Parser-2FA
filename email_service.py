
from email.message import EmailMessage
import smtplib

from app.config import settings


def is_email_configured() -> bool:
    return bool(settings.SMTP_EMAIL and settings.SMTP_PASSWORD)


def send_otp_email(email: str, otp: str):
    if not is_email_configured():
        return False

    message = EmailMessage()
    message["Subject"] = "AI Resume Parser - Email Verification"
    message["From"] = settings.SMTP_EMAIL
    message["To"] = email

    message.set_content(
        f"Your verification OTP is: {otp}\n"
        "This OTP is valid for 5 minutes."
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(message)

    return True
