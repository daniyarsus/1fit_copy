from src.models.user import User
from src.models.student import Student
from src.models.admin import Admin
from src.models.country import Country
from src.models.city import City
from src.models.university import University
from src.models.part import Part
from src.models.faculty import Faculty
from src.models.document import Document
from src.models.document_student import DocumentStudent
from src.models.student_notification import StudentNotification
from src.models.admin_notification import AdminNotification
from src.reposotories.repository import SQLAlchemyRepository
from src.models.student_application import StudentApplication
from src.models.check import Check
from src.models.check_student import CheckStudent


class UserRepository(SQLAlchemyRepository):
    model = User


class DocumentStudentRepository(SQLAlchemyRepository):
    model = DocumentStudent


class UniversityRepository(SQLAlchemyRepository):
    model = University


class CountryRepository(SQLAlchemyRepository):
    model = Country


class CityRepository(SQLAlchemyRepository):
    model = City


class AdminRepository(SQLAlchemyRepository):
    model = Admin


class StudentRepository(SQLAlchemyRepository):
    model = Student


class PartRepository(SQLAlchemyRepository):
    model = Part


class FacultyRepository(SQLAlchemyRepository):
    model = Faculty


class DocumentRepository(SQLAlchemyRepository):
    model = Document


class AdminNotificationRepository(SQLAlchemyRepository):
    model = AdminNotification


class StudentNotificationRepository(SQLAlchemyRepository):
    model = StudentNotification


class StudentApplicationRepository(SQLAlchemyRepository):
    model = StudentApplication


class CheckRepository(SQLAlchemyRepository):
    model = Check


class CheckStudentRepository(SQLAlchemyRepository):
    model = CheckStudent
