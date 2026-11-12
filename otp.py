
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class OTPChallenge(Base):
    __tablename__ = "otp_challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    otp_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
