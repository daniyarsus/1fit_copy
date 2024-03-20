from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, validator


class SendPasswordCodeSchema(BaseModel):
    email: EmailStr


class VerifyPasswordCodedSchema(BaseModel):
    email: EmailStr
    code: Annotated[int, None] = Field(..., ge=100000, le=999999)
    new_password: Annotated[str, None] = Field(..., min_length=8)
