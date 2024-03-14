from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func
from settings.database.database_connection import Base
from src.schemas.student_notification import StudentNotificationRead


class StudentNotification(Base):
    __tablename__ = "StudentNotification"
    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('Student.id', ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())

    def to_read_model(self):
        return StudentNotificationRead(
            id=self.id,
            student_id=self.id,
            text=self.text,
            created_at=self.created_at
        )
