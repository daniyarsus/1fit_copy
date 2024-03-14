from fastapi import (APIRouter,
                     Depends)

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.utils.dependencies.db import get_session

from src.api.v1.auth.services.signup import controllers
from src.api.v1.auth.services.signup import schemas


router = APIRouter()


@router.post(
    "/create-user",
    description="Эндпоинт создания пользователя."
)
async def register_user_endpoint(
        create_data: schemas.RegistrationSchema,
        db: AsyncSession = Depends(get_session)
):
    signup_controller = controllers.SignupController(
        db=db
    )
    return await signup_controller.create_user(
        create_data=create_data
    )


@router.post(
    "/send-email",
    description="Эндпоинт отправки почты для верификации пользователя."
)
async def send_verification_email_endpoint(
        send_data: schemas.SendConfirmationEmailSchema,
        db: AsyncSession = Depends(get_session)
):
    signup_controller = controllers.SignupController(
        db=db
    )
    return await signup_controller.send_confirmation_email(
        send_data=send_data
    )


@router.post(
    "/verify-email",
    description="Эндпоинт верификации кода из почты для верификации пользователя."
)
async def verify_verification_email_endpoint(
        verify_data: schemas.VerifyConfirmationEmailSchema,
        db: AsyncSession = Depends(get_session)
):
    signup_controller = controllers.SignupController(
        db=db
    )
    return await signup_controller.verify_confirmation_email(
        verify_data=verify_data
    )
