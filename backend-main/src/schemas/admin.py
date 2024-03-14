from pydantic import BaseModel


class AdminRead(BaseModel):
    id: int
    user_id: int
    role: str
    email: str

    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    user_id: int
    role: str

    class Config:
        from_attributes = True