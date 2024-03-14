from pydantic import BaseModel




class UniversityRead(BaseModel):
    id: int
    name: str
    city_id: int
    city_name: str
    faculties: list
    class Config:
        orm_mode = True


class UniversityCreate(BaseModel):
    name: str
    city_id: int

    class Config:
        from_attributes = True
