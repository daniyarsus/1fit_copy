from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.repository.base import AbstractRepository

from app.schemas.password import SendPasswordCodeSchema, VerifyPasswordCodedSchema

from app.settings.config import settings
from app.settings.redis.connection import redis_client_password

from app.utils.help.generate_code import generate_verification_code


class PasswordService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def send_code(self, data: SendPasswordCodeSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            code = generate_verification_code()

            existing_user = await self.users_repo.get_one(email=data.email)

            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователь с такой почтой не найден!"
                )

            if not existing_user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь не подтвержден!"
                )

            await redis_client_password.set(name=data.email, value=code, ex=120)

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

    async def verify_code(self, data: VerifyPasswordCodedSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            stored_code = await redis_client_password.get(data.email)
            if stored_code is None:
                raise HTTPException(status_code=404, detail="Код не был найден!")

            # Преобразуем код из запроса в строку
            input_code = str(data.code)

            if input_code != stored_code.decode("utf-8"):
                raise HTTPException(status_code=400, detail="Код не подходит!")

            await self.users_repo.edit_one({'password': data.new_password}, email=data.email)

            # Удаляем код подтверждения из Redis
            await redis_client_password.delete(data.email)

            return JSONResponse(
                status_code=200,
                content={"message": "Пароль успешно изменен!"}
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Произошла ошибка при проверке кода: {str(e)}"
            )
