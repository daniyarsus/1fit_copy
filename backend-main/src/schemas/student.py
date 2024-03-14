from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.schemas.status import StatusRead


class StudentRead(BaseModel):
    id: int
    user_id: int
    firstname: Optional[str]
    lastname: Optional[str]
    iin: Optional[str]
    father_name: Optional[str]
    mother_name: Optional[str]
    live_country: Optional[str]
    live_city: Optional[str]
    birthday: Optional[date]
    passport_number: Optional[str]
    passport_photo: Optional[str]
    phone_number: Optional[str]
    study_country_id: Optional[int]
    study_city_id: Optional[int]
    study_country: Optional[str]
    study_city: Optional[str]
    university_id: Optional[int]
    university: Optional[str]
    faculty_id: Optional[int]
    study_language: Optional[str]
    faculty: Optional[str]
    contract_number: Optional[str]
    contract_date: Optional[date]
    full_price: Optional[int]
    paid_price: Optional[int]
    parent_phone_number: str
    photo_path: Optional[str]
    status_id: Optional[int]
    address: Optional[str]
    status: Optional[StatusRead]
    year: Optional[int]
    gpa: Optional[float]
    email: Optional[EmailStr]
    underage: Optional[bool]

    class Config:
        from_attributes = True


class StudentCreateInput(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    father_name: str
    mother_name: str
    live_country: str
    live_city: str
    birthday: date
    passport_number: str
    phone_number: str
    parent_phone_number: str
    address: str

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    father_name: str
    mother_name: str
    live_country: str
    live_city: str
    birthday: date
    passport_number: str
    phone_number: str
    parent_phone_number: str
    address: str

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    father_name: str
    mother_name: str
    live_country: str
    live_city: str
    birthday: date
    passport_number: str
    phone_number: str
    parent_phone_number: str
    address: str

    class Config:
        from_attributes = True





class AdminStudentUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    father_name: Optional[str]
    mother_name: Optional[str]
    live_country: Optional[str]
    live_city: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    study_country_id: Optional[int]
    study_city_id: Optional[int]
    full_price: Optional[int]
    paid_price: Optional[int]
    parent_phone_number: str
    photo_path: Optional[str]
    address: Optional[str]
    status_id: Optional[int]
    iin: Optional[str]
    contract_number: Optional[str]
    contract_date: Optional[date]
    university_id: Optional[int]
    faculty_id: Optional[int]
    year: Optional[int]
    study_language: Optional[str]
    gpa: Optional[float]

    class Config:
        from_attributes = True



class AdminStudentCreateInput(BaseModel):
    email: str
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    father_name: Optional[str]
    mother_name: Optional[str]
    live_country: Optional[str]
    live_city: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    study_country_id: Optional[int]
    study_city_id: Optional[int]
    full_price: Optional[int]
    paid_price: Optional[int]
    parent_phone_number: str
    photo_path: Optional[str]
    address: Optional[str]
    status_id: Optional[int]
    iin: Optional[str]
    contract_number: Optional[str]
    contract_date: Optional[date]
    university_id: Optional[int]
    faculty_id: Optional[int]
    year: Optional[int]
    study_language: Optional[str]
    gpa: Optional[float]

    class Config:
        from_attributes = True


class AdminStudentCreate(BaseModel):
    user_id: int
    firstname: Optional[str]
    lastname: Optional[str]
    father_name: Optional[str]
    mother_name: Optional[str]
    live_country: Optional[str]
    live_city: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    study_country_id: Optional[int]
    study_city_id: Optional[int]
    full_price: Optional[int]
    paid_price: Optional[int]
    parent_phone_number: str
    photo_path: Optional[str]
    address: Optional[str]
    status_id: Optional[int]
    iin: Optional[str]
    contract_number: Optional[str]
    contract_date: Optional[date]
    university_id: Optional[int]
    faculty_id: Optional[int]
    year: Optional[int]
    study_language: Optional[str]
    gpa: Optional[float]

    class Config:
        from_attributes = True