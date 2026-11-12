
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User

from app.schemas.auth import (
    TOTPSetupResponse,
    TOTPVerifyRequest,
    OTPVerifyResponse
)

from app.services.totp_service import (
    generate_totp_secret,
    get_totp_uri,
    verify_totp
)

from app.services.security import create_access_token


router = APIRouter(
    prefix="/api/v1/auth/totp",
    tags=["Browser TOTP Authentication"]
)


@router.post("/setup/{user_id}", response_model=TOTPSetupResponse)
async def setup_totp(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="User is already verified"
        )

    if not user.totp_secret:
        user.totp_secret = generate_totp_secret()
        await db.commit()
        await db.refresh(user)

    provisioning_uri = get_totp_uri(
        user.totp_secret,
        user.email
    )

    return {
        "message": "TOTP setup successful. Add the account to your authenticator app.",
        "secret": user.totp_secret,
        "provisioning_uri": provisioning_uri
    }


@router.post("/verify", response_model=OTPVerifyResponse)
async def verify_totp_code(
    data: TOTPVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == data.user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="User is already verified"
        )

    if not user.totp_secret:
        raise HTTPException(
            status_code=400,
            detail="TOTP setup is required first"
        )

    if not verify_totp(user.totp_secret, data.otp):
        raise HTTPException(
            status_code=400,
            detail="Invalid TOTP code"
        )

    user.totp_enabled = True
    user.is_verified = True
    user.is_active = True

    await db.commit()

    access_token = create_access_token(user.id)

    return {
        "message": "Browser TOTP verified successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }

