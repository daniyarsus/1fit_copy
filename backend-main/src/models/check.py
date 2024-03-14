from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.check import CheckRead



class Check(Base):
    __tablename__ = "Check"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('Country.id'), nullable=False)
    country = relationship('Country', back_populates='checks')
    def to_read_model(self) -> CheckRead:
        return CheckRead(
            id=self.id,
            name=self.name,
            country_id=self.country_id,
        )
