from typing import Annotated, Union

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.register import RegisterSchema, SendEmailCodeSchema, VerifyEmailCodeSchema
from app.service.register import RegisterService
from app.api.dependencies import register_service

from app.schemas.logout import LogoutSchema
from app.service.logout import LogoutService
from app.api.dependencies import logout_service

from app.schemas.password import SendPasswordCodeSchema, VerifyPasswordCodedSchema
from app.service.password import PasswordService
from app.api.dependencies import password_service


router = APIRouter()


@router.post(
    "/signup/register",
)
async def register_user_endpoint(
        data: RegisterSchema,
        users_service: Annotated[RegisterService, Depends(register_service)]
):
    result = await users_service.register_user(data)
    return result


@router.post(
    "/signup/send-code"
)
async def send_code_endpoint(
        data: SendEmailCodeSchema,
        users_service: Annotated[RegisterService, Depends(register_service)]
):
    result = await users_service.send_code(data)
    return result


@router.post(
    "/signup/verify-code"
)
async def verify_code_endpoint(
        data: VerifyEmailCodeSchema,
        users_service: Annotated[RegisterService, Depends(register_service)]
):
    result = await users_service.veriify_code(data)
    return result


#@router.post(
#   "/signin/token"
#)
#async def create_token_endpoint():
#    ...


@router.post("/jwt-create")
# Функция для создания JWT токена с ролью в виде целого числа и именем пользователя
def create_jwt_token(id: int, username: str, role: int, expires_delta: Union[timedelta, int] = 36000):
    # Определите ваш секретный ключ
    SECRET_KEY = "fuosdp82ipo21epoqwpoe129fdspom12"
    # Определите алгоритм шифрования
    ALGORITHM = "HS256"
    # Преобразуйте expires_delta в timedelta, если он представлен в секундах
    if isinstance(expires_delta, int):
        expires_delta = timedelta(seconds=expires_delta)
    # Определите время истечения токена
    expire = datetime.utcnow() + expires_delta
    # Подготовьте данные для токена
    to_encode = {"id": id, "username": username, "role": role, "exp": expire}
    # Подпишите и верните токен
    from jose import jwt
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post(
    "/password/send-code"
)
async def change_password_endpoint(
        data: SendPasswordCodeSchema,
        users_service: Annotated[PasswordService, Depends(password_service)]
):
    result = await users_service.send_code(data)
    return result


@router.post(
    "/password/verify-code"
)
async def change_password_endpoint(
        data: VerifyPasswordCodedSchema,
        users_service: Annotated[PasswordService, Depends(password_service)]
):
    result = await users_service.verify_code(data)
    return result


@router.post(
    "/logout/del-jwt"
)
async def logout_user_endpoint(
        data: LogoutSchema,
        users_service: Annotated[LogoutService, Depends(logout_service)]
):
    result = await users_service.logout_user(data)
    return result
