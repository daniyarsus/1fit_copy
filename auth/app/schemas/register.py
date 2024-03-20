from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    username: Annotated[str, None] = Field(..., min_length=1, max_length=25)
    password: Annotated[str, None] = Field(..., min_length=8, max_length=25)
    email: EmailStr
    phone: Annotated[int, None] = Field(..., ge=80000000000, le=99999999999)


class SendEmailCodeSchema(BaseModel):
    email: EmailStr


class VerifyEmailCodeSchema(BaseModel):
    email: EmailStr
    code: Annotated[int, None] = Field(...)
