
import secrets
from pwdlib import PasswordHash

otp_hasher = PasswordHash.recommended()


def generate_otp() -> str:
    return f"{secrets.randbelow(1000000):06d}"


def hash_otp(otp: str) -> str:
    return otp_hasher.hash(otp)


def verify_otp(otp: str, hashed_otp: str) -> bool:
    return otp_hasher.verify(otp, hashed_otp)
