from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app.models import User, UserResume, OTPChallenge
from app.routers.resume import router as resume_router
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.dashboard import router as dashboard_router
from app.routers.totp import router as totp_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="AI Resume Parser & 2FA Pipeline",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(resume_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(totp_router)

@app.get("/")
async def home():
    return {
        "message": "AI Resume Parser API is running!"
    }