from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func, Boolean, String
from sqlalchemy.orm import relationship
from settings.database.database_connection import Base
from src.models.document_student import DocumentStudent
from src.models.student import Student
from src.models.document import Document
from src.models.student_application import StudentApplication
from src.schemas.admin_notification import AdminNotificationRead


class AdminNotification(Base):
    __tablename__ = "AdminNotification"

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('Student.id'), nullable=True)
    student = relationship('Student', lazy='selectin')
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    checked = Column(Boolean, default=False)
    type = Column(String, nullable=False)  # student, document, application

    # for document
    document_student_id = Column(ForeignKey('DocumentStudent.id', ondelete='CASCADE'), nullable=True)
    document_student = relationship(DocumentStudent, lazy='selectin')
    # for application
    student_application_id = Column(ForeignKey('StudentApplication.id', ondelete='CASCADE'), nullable=True)
    student_application = relationship(StudentApplication, lazy='selectin')
    def to_read_model(self):
        return AdminNotificationRead(
            id=self.id,
            student_id=self.student_id,
            student_firstname=self.student.firstname,
            student_lastname=self.student.lastname,
            text=self.text,
            created_at=self.created_at,
            checked=self.checked,
            type=self.type,
            document_id=self.document_student.document.id if self.document_student else None,
            student_document_id=self.document_student.id if self.document_student else None,
            document_name=self.document_student.document.name if self.document_student else None,
            document_file_path=self.document_student.file_path if self.document_student else None,
            student_application_id=self.student_application_id,
            application_name=self.student_application.application_name if self.student_application else None,
            application_file_path=self.student_application.file_path if self.student_application else None,
            application_created_at=self.student_application.created_at if self.student_application else None
        )
