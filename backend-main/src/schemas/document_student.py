from typing import Optional

from pydantic import BaseModel

from src.schemas.document import DocumentRead
from src.schemas.student import StudentRead


class DocumentStudentRead(BaseModel):
    student: Optional[StudentRead]
    document: Optional[DocumentRead]
    id: int
    file_path: Optional[str] = None
    correct: Optional[bool] = None

    class Config:
        from_attributes = True


class DocumentStudentCreate(BaseModel):
    student_id: int
    document_id: int
    file_path: str
    correct: Optional[bool] = None

    class Config:
        from_attributes = True