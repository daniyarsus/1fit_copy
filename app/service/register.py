from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.repository.base import AbstractRepository

from app.schemas.register import RegisterSchema, SendEmailCodeSchema, VerifyEmailCodeSchema

from app.settings.config import settings
from app.settings.redis.connection import redis_client_register

from app.utils.help.generate_code import generate_verification_code


class RegisterService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def register_user(self, data: RegisterSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            existing_username = await self.users_repo.get_one(username=data.username)
            existing_email = await self.users_repo.get_one(email=data.email)
            existing_phone = await self.users_repo.get_one(phone=data.phone)

            if existing_username or existing_email or existing_phone:
                raise HTTPException(
                    status_code=400,
                    detail="Пользовать с такими данными уже существует!"
                )

            user_dict = data.dict()
            result = await self.users_repo.add_one(user_dict)
            if result:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Пользователь зарегистрирован успешно!"
                    }
                )

        except Exception as e:
            return HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def send_code(self, data: SendEmailCodeSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            code = generate_verification_code()

            existing_user = await self.users_repo.get_one(email=data.email)

            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователь с такой почтой не найден!"
                )

            if existing_user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail="Почта уже верифицирована!"
                )

            await redis_client_register.set(name=data.email, value=code, ex=120)

            # Отправка письма
            message = f"Код подтверждения: {str(code)}"
            msg = MIMEMultipart()
            msg['From'] = settings.smtp_config.EMAIL_FROM
            msg['To'] = data.email
            msg['Subject'] = "Ваш код подтверждения"
            msg.attach(MIMEText(message, 'plain', 'utf-8'))

            server = smtplib.SMTP(settings.smtp_config.DOMAIN_NAME, settings.smtp_config.SMTP_PORT)
            server.starttls()
            server.login(settings.smtp_config.EMAIL_FROM, settings.smtp_config.API_KEY)
            server.send_message(msg)
            server.quit()

            return JSONResponse(
                status_code=200,
                content={
                    "message": "Письмо с кодом отправлено успешно!"
                }
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def verify_code(self, data: VerifyEmailCodeSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            stored_code = await redis_client_register.get(data.email)
            if stored_code is None:
                raise HTTPException(
                    status_code=404,
                    detail="Код не был найден!"
                )

            # Преобразуем код из запроса в строку
            input_code = str(data.code)

            if input_code != stored_code.decode("utf-8"):
                raise HTTPException(status_code=400, detail="Код не подходит!")

            await self.users_repo.edit_one({'is_verified': True}, email=data.email)

            # Удаляем код подтверждения из Redis
            await redis_client_register.delete(data.email)

            return JSONResponse(
                status_code=200,
                content={"message": "Пользователь подтвержден!"}
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
