from pydantic import BaseModel


class CheckRead(BaseModel):
    id: int
    name: str
    country_id: int

    class Config:
        from_attributes = True


class CheckCreate(BaseModel):
    name: str
    country_id: int

    class Config:
        from_attributes = True
