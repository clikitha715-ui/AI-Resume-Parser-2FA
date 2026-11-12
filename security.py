
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone

from app.config import settings

password_hash = PasswordHash.recommended()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
