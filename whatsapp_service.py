
import base64
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from app.config import settings


def send_whatsapp_otp(phone: str, otp: str) -> bool:
    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    whatsapp_from = getattr(settings, "TWILIO_WHATSAPP_FROM", "")

    if not account_sid or not auth_token or not whatsapp_from:
        return False

    url = (
        f"https://api.twilio.com/2010-04-01/"
        f"Accounts/{account_sid}/Messages.json"
    )

    message_data = {
        "From": whatsapp_from,
        "To": f"whatsapp:{phone}",
        "Body": (
            f"Your AI Resume Parser verification OTP is {otp}. "
            "It is valid for 5 minutes."
        )
    }

    credentials = base64.b64encode(
        f"{account_sid}:{auth_token}".encode()
    ).decode()

    request = Request(
        url,
        data=urlencode(message_data).encode(),
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urlopen(request, timeout=15) as response:
            return response.status == 201
    except (HTTPError, Exception):
        return False
