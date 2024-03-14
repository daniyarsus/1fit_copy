from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class StudentNotificationRead(BaseModel):
    id: int
    student_id: int
    text: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class StudentNotificationCreate(BaseModel):
    student_id: int
    text: str

    class Config:
        from_attributes = True