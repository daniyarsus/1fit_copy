from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date

from settings.database.database_connection import Base
from src.models.faculty import Faculty
from src.models.status import Status
from src.models.university import University
from src.models.user import User
from src.models.city import City
from src.models.country import Country
from src.schemas.student import StudentRead


class Student(Base):
    __tablename__ = 'Student'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    father_name = Column(String, nullable=True)
    mother_name = Column(String, nullable=True)
    live_country = Column(String, nullable=True)
    live_city = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    passport_number = Column(String, nullable=True)
    passport_photo = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    study_country_id = Column(ForeignKey('Country.id'), nullable=True)
    study_city_id = Column(ForeignKey('City.id'), nullable=True)
    university_id = Column(ForeignKey('University.id'), nullable=True)
    faculty_id = Column(ForeignKey('Faculty.id'), nullable=True)
    contract_number = Column(String, nullable=True)
    contract_date = Column(Date, nullable=True)
    full_price = Column(Integer, nullable=True)
    paid_price = Column(Integer, nullable=True)
    parent_phone_number = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)
    address = Column(String, nullable=True)
    study_language = Column(String, nullable=True)
    status_id = Column(ForeignKey('Status.id'), nullable=True, default=1)
    iin = Column(String, nullable=True)
    year = Column(Integer, nullable=True, default=int(datetime.now().year))
    gpa = Column(Float, nullable=True)
    user = relationship(User, lazy="selectin")
    study_country = relationship(Country, lazy="selectin")
    study_city = relationship(City, lazy="selectin")
    status = relationship(Status, lazy="selectin")
    university = relationship(University, lazy="selectin")
    faculty = relationship(Faculty, lazy="selectin")

    def to_read_model(self) -> StudentRead:
        user_birthday = datetime.combine(self.birthday, datetime.min.time())

        # Рассчитываем возраст пользователя на 1 сентября 2024 года
        age = (datetime(2024, 9, 1) - user_birthday).days // 365

        if age >= 18:
            underage = False
        else:
            underage = True

        return StudentRead(
            id=self.id,
            user_id=self.user_id,
            firstname=self.firstname,
            lastname=self.lastname,
            father_name=self.father_name,
            mother_name=self.mother_name,
            live_country=self.live_country,
            live_city=self.live_city,
            birthday=self.birthday,
            passport_number=self.passport_number,
            passport_photo=self.passport_photo,
            full_price=self.full_price,
            paid_price=self.paid_price,
            phone_number=self.phone_number,
            study_country_id=self.study_country_id,
            study_city_id=self.study_city_id,
            study_country=self.study_country.name if self.study_country else None,
            study_city=self.study_city.name if self.study_city else None,
            university_id=self.university_id,
            faculty_id=self.faculty_id,
            contract_number=self.contract_number,
            contract_date=self.contract_date,
            university=self.university.name if self.university else None,
            faculty=self.faculty.name if self.faculty else None,
            parent_phone_number=self.parent_phone_number,
            photo_path=self.photo_path,
            address=self.address,
            study_language=self.study_language,
            status_id=self.status_id,
            year=self.year,
            gpa=self.gpa,
            status=self.status.to_read_model() if self.status else None,
            email=self.user.email,
            iin=self.iin,
            underage=underage
        )
