from app.repository.user import UserRepository

from app.service.register import RegisterService
from app.service.logout import LogoutService
from app.service.password import PasswordService


def register_service():
    return RegisterService(UserRepository)


def logout_service():
    return LogoutService


def password_service():
    return PasswordService(UserRepository)

