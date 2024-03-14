from src.reposotories.all_repositories import UserRepository, StudentRepository, \
    AdminRepository, CountryRepository, CityRepository, UniversityRepository, PartRepository, FacultyRepository, \
    DocumentRepository, DocumentStudentRepository, StudentNotificationRepository, AdminNotificationRepository, \
    StudentApplicationRepository, CheckRepository, CheckStudentRepository
from src.services.document_student import DocumentStudentService
from src.services.user import UserService
from src.services.student import StudentService
from src.services.admin import AdminService
from src.services.country import CountryService
from src.services.city import CityService
from src.services.university import UniversityService
from src.services.faculty import FacultyService
from src.services.part import PartService
from src.services.document import DocumentService
from src.services.student_notification import StudentNotificationService
from src.services.admin_notification import AdminNotificationService
from src.services.student_application import StudentApplicationService
from src.services.check import CheckService
from src.services.check_student import CheckStudentService


def check_service():
    return CheckService(CheckRepository())


def check_student_service():
    return CheckStudentService(CheckStudentRepository())


def user_service():
    return UserService(UserRepository())


def part_service():
    return PartService(PartRepository())


def country_service():
    return CountryService(CountryRepository())


def city_service():
    return CityService(CityRepository())


def student_service():
    return StudentService(StudentRepository())


def admin_service():
    return AdminService(AdminRepository())


def university_service():
    return UniversityService(UniversityRepository())


def faculty_service():
    return FacultyService(FacultyRepository())


def document_service():
    return DocumentService(DocumentRepository())


def document_student_service():
    return DocumentStudentService(DocumentStudentRepository())


def student_notification_service():
    return StudentNotificationService(StudentNotificationRepository())


def admin_notification_service():
    return AdminNotificationService(AdminNotificationRepository())


def student_application_service():
    return StudentApplicationService(StudentApplicationRepository())
