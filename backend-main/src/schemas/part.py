from pydantic import BaseModel
from typing import Optional


class PartRead(BaseModel):
    id: int
    name: str
    country_id: int
    translated: Optional[bool]
    documents: list
    moderator: Optional[bool]
    underage: Optional[bool]

    class Config:
        from_attributes = True

class PartCreate(BaseModel):
    name: str
    country_id: int
    translated: Optional[bool]
    moderator: Optional[bool]
    underage: Optional[bool]

    class Config:
        from_attributes = True
