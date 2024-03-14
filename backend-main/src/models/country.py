from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.models.check import Check
from src.schemas.city import CityRead
from src.schemas.country import CountryRead
from src.models.part import Part
from src.schemas.part import PartRead


class Country(Base):
    __tablename__ = "Country"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cities = relationship('City', back_populates='country', lazy="selectin")
    parts = relationship(Part, back_populates='country', lazy="selectin")
    checks = relationship(Check, back_populates='country', lazy="selectin")
    def to_read_model(self) -> CountryRead:
        cities_read = [city.to_read_model() for city in self.cities]
        parts_read = [part.to_read_model() for part in self.parts]
        checks_read = [check.to_read_model() for check in self.checks]

        return CountryRead(
            id=self.id,
            name=self.name,
            cities=cities_read,
            parts=parts_read,
            checks=checks_read
        )