from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    email: str
    role_id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class LoginInput(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class LoginOutput(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

    class Config:
        from_attributes = True


class RefreshInput(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True


class RefreshOutput(BaseModel):
    access_token: str
    token_type: str


    class Config:
        from_attributes = True