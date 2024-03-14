from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseRegistrationSchema(BaseModel):
    class Config:
        from_attributes = True


class RegistrationSchema(BaseRegistrationSchema):
    username: Optional[str]
    password: Optional[str]
    phone: Optional[int]
    email: EmailStr


class SendConfirmationEmailSchema(BaseRegistrationSchema):
    email: EmailStr


class VerifyConfirmationEmailSchema(BaseRegistrationSchema):
    email: EmailStr
    code: Optional[int]
