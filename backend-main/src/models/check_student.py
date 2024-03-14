from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.check_student import CheckStudentRead


class CheckStudent(Base):
    __tablename__ = "CheckStudent"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.id', ondelete='CASCADE'))
    check_id = Column(Integer, ForeignKey('Check.id', ondelete='CASCADE'))
    check_file_path = Column(Text, nullable=True)
    price_usd = Column(Integer, nullable=True)
    price_kzt = Column(Integer, nullable=True)
    student = relationship('Student', lazy='selectin')
    check = relationship('Check', lazy='selectin')

    def to_read_model(self) -> CheckStudentRead:
        return CheckStudentRead(
            id=self.id,
            student_id=self.student.id,
            student_firstname=self.student.firstname,
            student_lastname=self.student.lastname,
            check=self.check.to_read_model(),
            price_usd=self.price_usd,
            price_kzt=self.price_kzt,
            check_file_path=self.check_file_path
        )