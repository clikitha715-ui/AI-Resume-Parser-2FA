
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal


class UserRegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(min_length=8)


class UserRegisterResponse(BaseModel):
    message: str
    user_id: int
    verification_channel: Literal["email", "whatsapp", "browser"]


class OTPVerifyRequest(BaseModel):
    user_id: int
    otp: str = Field(min_length=6, max_length=6)


class OTPVerifyResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"


class TOTPSetupResponse(BaseModel):
    message: str
    secret: str
    provisioning_uri: str


class TOTPVerifyRequest(BaseModel):
    user_id: int
    otp: str = Field(min_length=6, max_length=6)
