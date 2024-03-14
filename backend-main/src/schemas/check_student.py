from typing import Optional

from pydantic import BaseModel

from src.schemas.check import CheckRead


class CheckStudentRead(BaseModel):
    id: int
    student_id: int
    student_firstname: str
    student_lastname: str
    check: CheckRead
    price_usd: Optional[int]
    price_kzt: Optional[int]
    check_file_path: Optional[str]

    class Config:
        from_attributes = True


class CheckStudentCreate(BaseModel):
    student_id: int
    check_id: int
    price_usd: Optional[int]
    price_kzt: Optional[int]
    check_file_path: Optional[str]

    class Config:
        from_attributes = True