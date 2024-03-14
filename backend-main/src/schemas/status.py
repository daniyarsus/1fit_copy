from typing import List

from pydantic import BaseModel


class StatusRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StatusCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True
