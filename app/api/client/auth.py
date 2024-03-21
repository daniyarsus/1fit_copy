from typing import Annotated, Union

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.utils.help.current_user import get_current_user

from app.schemas.register import RegisterSchema, SendEmailCodeSchema, VerifyEmailCodeSchema
from app.service.register import RegisterService
from app.api.dependencies import register_service

from app.schemas.login import LoginPhoneSchema, LoginEmailSchema, LoginUsernameSchema, UpdateRefreshTokenSchema
from app.service.login import LoginService
from app.api.dependencies import login_service

from app.schemas.password import SendPasswordCodeSchema, VerifyPasswordCodedSchema
from app.service.password import PasswordService
from app.api.dependencies import password_service

from app.schemas.logout import LogoutSchema
from app.service.logout import LogoutService
from app.api.dependencies import logout_service


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
    result = await users_service.verify_code(data)
    return result


@router.post(
   "/signin/token-username"
)
async def create_token_endpoint(
        data: LoginUsernameSchema,
        users_service: Annotated[LoginService, Depends(login_service)]
):
    result = await users_service.login_by_username(data)
    return result


@router.post(
   "/signin/token-email"
)
async def create_token_endpoint(
        data: LoginEmailSchema,
        users_service: Annotated[LoginService, Depends(login_service)]
):
    result = await users_service.login_by_email(data)
    return result


@router.post(
   "/signin/token-phone"
)
async def create_token_endpoint(
        data: LoginPhoneSchema,
        users_service: Annotated[LoginService, Depends(login_service)]
):
    result = await users_service.login_by_phone(data)
    return result


@router.post("/signin/update-refresh-token")
async def update_refresh_token_endpoint(
        data: UpdateRefreshTokenSchema,
        users_service: Annotated[LoginService, Depends(login_service)]
):
    result = await users_service.update_refresh_token(data)
    return result


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
    "/logout/del-token"
)
async def logout_user_endpoint(
        data: LogoutSchema,
        users_service: Annotated[LogoutService, Depends(logout_service)],
        current_user: Annotated[dict, Depends(get_current_user)]
):
    result = await users_service.logout_user(data)
    return result
