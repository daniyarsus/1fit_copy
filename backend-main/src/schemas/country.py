from typing import List

from pydantic import BaseModel

from src.schemas.check import CheckRead
from src.schemas.city import CityRead
from src.schemas.part import PartRead


class CountryRead(BaseModel):
    id: int
    name: str
    cities: List[CityRead]  # Используйте CityRead вместо City
    parts: List[PartRead]
    checks: List[CheckRead]

    class Config:
        from_attributes = True


class CountryCreate(BaseModel):
    name: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
