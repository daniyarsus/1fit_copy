from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.part import PartRead


class Part(Base):
    __tablename__ = "Part"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('Country.id', ondelete='CASCADE'), nullable=False)
    country = relationship('Country', back_populates='parts')
    translated = Column(Boolean, default=False)
    underage = Column(Boolean, default=False)
    moderator = Column(Boolean, default=False)
    documents = relationship('Document', back_populates='part', lazy='selectin')
    def to_read_model(self) -> PartRead:
        documents = [document.to_read_model() for document in self.documents]
        return PartRead(
            id=self.id,
            name=self.name,
            country_id=self.country_id,
            translated=self.translated,
            moderator=self.moderator,
            underage=self.underage,
            documents=documents
        )