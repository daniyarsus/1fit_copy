from datetime import datetime

from pydantic import BaseModel


class StudentApplicationRead(BaseModel):
    id: int
    student_id: int
    student_firstname: str
    student_lastname: str
    application_name: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class StudentApplicationCreate(BaseModel):
    student_id: int
    application_name: str
    file_path: str
    class Config:
        from_attributes = True


class StudentApplicationCreateWithFile(BaseModel):
    id: int
    student_id: int
    application_name: str
    file_path: str

    class Config:
        from_attributes = True