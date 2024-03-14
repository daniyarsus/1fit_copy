from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func, Boolean, String
from sqlalchemy.orm import relationship
from settings.database.database_connection import Base
from src.models.student import Student
from src.schemas.student_application import StudentApplicationRead


class StudentApplication(Base):
    __tablename__ = "StudentApplication"
    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('Student.id', ondelete='CASCADE'), nullable=True)
    student = relationship(Student, lazy='selectin')
    application_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    def to_read_model(self):
        return StudentApplicationRead(
            id=self.id,
            student_id=self.student_id,
            student_firstname=self.student.firstname,
            student_lastname=self.student.lastname,
            application_name=self.application_name,
            file_path=self.file_path,
            created_at=self.created_at
        )

