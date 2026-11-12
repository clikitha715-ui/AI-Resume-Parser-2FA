
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.database import get_db
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest
from app.services.security import SECRET_KEY, ALGORITHM


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Student Profile"]
)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user or not user.is_active or not user.is_verified:
        raise HTTPException(
            status_code=401,
            detail="User is not authorized"
        )

    return user


# GET STUDENT PROFILE
@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# UPDATE STUDENT PROFILE
@router.patch("/", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user
