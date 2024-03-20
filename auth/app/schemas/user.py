from pydantic import BaseModel, EmailStr


class ReadUserModel(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    phone: int
    is_verified: bool

    class Config:
        from_attributes = True


