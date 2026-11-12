
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )

    phone: Mapped[str] = mapped_column(
        String(20), nullable=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    verification_channel: Mapped[str] = mapped_column(
        String(20), nullable=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    totp_secret: Mapped[str] = mapped_column(
        String(32), nullable=True
    )

    totp_enabled: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
