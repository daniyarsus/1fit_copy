from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class AdminNotificationRead(BaseModel):
    id: int
    student_id: int
    student_firstname: str
    student_lastname: str
    text: str
    created_at: datetime
    checked: Optional[bool]
    type: Optional[str] = None
    document_id: Optional[int] = None
    document_name: Optional[str] = None
    document_file_path: Optional[str] = None
    student_document_id: Optional[int] = None
    student_application_id: Optional[int] = None
    application_name: Optional[str] = None
    application_file_path: Optional[str] = None
    application_created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminNotificationCreate(BaseModel):
    student_id: Optional[int]
    text: str
    type: Optional[str] = None
    document_student_id: Optional[int] = None
    student_application_id: Optional[int] = None

    class Config:
        from_attributes = True