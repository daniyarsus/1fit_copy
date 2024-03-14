from pydantic import BaseModel


class FacultyRead(BaseModel):
    id: int
    name: str
    university_id: int

    class Config:
        from_attributes = True


class FacultyCreate(BaseModel):
    name: str
    university_id: int

    class Config:
        from_attributes = True
