
from fastapi import APIRouter, Depends

from app.models.user import User
from app.routers.profile import get_current_user


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Student Dashboard"]
)


@router.get("/student")
async def student_dashboard(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Welcome to the Student Dashboard!",
        "user_id": current_user.id,
        "name": current_user.full_name,
        "email": current_user.email,
        "status": "Verified Student",
        "dashboard": "/dashboard/student"
    }
