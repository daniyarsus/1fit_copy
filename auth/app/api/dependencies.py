from app.repository.user import UserRepository

from app.service.register import RegisterService
from app.service.login import LoginService
from app.service.password import PasswordService
from app.service.logout import LogoutService


def register_service():
    return RegisterService(UserRepository)


def login_service():
    return LoginService(UserRepository)


def password_service():
    return PasswordService(UserRepository)


def logout_service():
    return LogoutService
