from pydantic import BaseModel


class CityRead(BaseModel):
    id: int
    name: str
    country_id: int
    universities: list

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    name: str
    country_id: int

    class Config:
        from_attributes = True
