from src.api.v1.admin.application import admin_student_application_router
from src.api.v1.admin.faculty import admin_faculty_router
from src.api.v1.admin.notification import admin_notification_router
from src.api.v1.admin.student_document import admin_document_student_router
from src.api.v1.auth import auth_router
from src.api.v1.student.check import student_check_router
from src.api.v1.student.student import student_student_router
from src.api.v1.admin.student import admin_student_router
from src.api.v1.admin.country import admin_country_router
from src.api.v1.admin.city import admin_city_router
from src.api.v1.admin.university import admin_university_router
from src.api.v1.admin.part import admin_part_router
from src.api.v1.admin.document import admin_document_router
from src.api.v1.student.document import student_document_router
from src.api.v1.student.notification import student_notification_router
from src.api.v1.student.application import student_application_router
from src.api.v1.admin.check import admin_check_router
from src.api.v1.admin.check_student import admin_check_student_router

all_routers = [
    auth_router,
    student_student_router,
    student_document_router,
    student_notification_router,
    student_check_router,
    student_application_router,
    admin_student_router,
    admin_country_router,
    admin_city_router,
    admin_university_router,
    admin_part_router,
    admin_faculty_router,
    admin_document_router,
    admin_notification_router,
    admin_document_student_router,
    admin_check_router,
    admin_check_student_router,
    admin_student_application_router
]
