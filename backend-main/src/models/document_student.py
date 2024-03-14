from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.document_student import DocumentStudentRead


class DocumentStudent(Base):
    __tablename__ = "DocumentStudent"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.id', ondelete='CASCADE'))
    document_id = Column(Integer, ForeignKey('Document.id', ondelete='CASCADE'))
    file_path = Column(Text, nullable=True)
    student = relationship('Student', lazy='selectin')
    document = relationship('Document', lazy='selectin')
    correct = Column(Boolean, nullable=True)
    def to_read_model(self) -> DocumentStudentRead:
        return DocumentStudentRead(
            id=self.id,
            file_path=self.file_path,
            student=self.student.to_read_model(),
            document=self.document.to_read_model(),
            correct=self.correct
        )