from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.faculty import FacultyRead



class Faculty(Base):
    __tablename__ = "Faculty"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    university_id = Column(Integer, ForeignKey('University.id', ondelete='CASCADE'))
    university = relationship('University', back_populates='faculties')

    def to_read_model(self) -> FacultyRead:
        return FacultyRead(
            id=self.id,
            name=self.name,
            university_id=self.university_id,
        )
