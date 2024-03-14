from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.document import DocumentRead


class Document(Base):
    __tablename__ = "Document"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    part_id = Column(Integer, ForeignKey('Part.id', ondelete='CASCADE'))
    part = relationship('Part', back_populates='documents', lazy='selectin')
    def to_read_model(self) -> DocumentRead:
        return DocumentRead(
            id=self.id,
            name=self.name,
            part_id=self.part_id,
        )