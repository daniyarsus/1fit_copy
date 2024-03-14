from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.city import CityRead



class City(Base):
    __tablename__ = "City"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('Country.id', ondelete='CASCADE'), nullable=False)
    country = relationship('Country', back_populates='cities')
    universities = relationship('University', back_populates='city', lazy="selectin")
    def to_read_model(self) -> CityRead:
        return CityRead(
            id=self.id,
            name=self.name,
            country_id=self.country_id,
            universities=[university.to_read_model() for university in self.universities]
        )
