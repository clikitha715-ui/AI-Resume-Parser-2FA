
from pydantic import BaseModel
from typing import Optional


class ResumeParseResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = []
    experience: Optional[str] = None
