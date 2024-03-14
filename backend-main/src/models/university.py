from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.university import UniversityRead
from src.models.faculty import Faculty


class University(Base):
    __tablename__ = "University"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('City.id', ondelete='CASCADE'))
    city = relationship('City', back_populates='universities', lazy='selectin')
    faculties = relationship(Faculty, back_populates='university', lazy='selectin')

    def to_read_model(self) -> UniversityRead:
        return UniversityRead(
            id=self.id,
            name=self.name,
            city_id=self.city_id,
            city_name=self.city.name,
            faculties=[faculty.to_read_model() for faculty in self.faculties]
        )
