from typing import Optional

from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: int
    name: str
    part_id: int

    class Config:
        from_attributes = True


class DocumentReadWithFile(BaseModel):
    id: int
    name: str
    part_id: int
    file_path: Optional[str] = None
    correct: Optional[bool]

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    name: str
    part_id: int

    class Config:
        from_attributes = True