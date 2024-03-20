from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


class LoginUsernameSchema(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=25)]
    password: Annotated[str, Field(min_length=8, max_length=25)]


class LoginEmailSchema(BaseModel):
    email: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(min_length=8, max_length=25)]


class LoginPhoneSchema(BaseModel):
    phone: Annotated[int, Field(ge=80000000000, le=99999999999)]
    password: Annotated[str, Field(min_length=8, max_length=25)]


class UpdateRefreshTokenSchema(BaseModel):
    jwt: Annotated[str, Field(...)]
