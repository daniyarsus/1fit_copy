from abc import abstractmethod, ABC

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from auth.app import models
from auth.app.signup import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseSignupController(ABC):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def create_user(self, create_data: schemas.RegistrationSchema):
        raise NotImplementedError

    @abstractmethod
    async def send_confirmation_email(self, send_data: schemas.SendConfirmationEmailSchema):
        raise NotImplementedError

    @abstractmethod
    async def verify_confirmation_email(self, verify_data: schemas.VerifyConfirmationEmailSchema):
        raise NotImplementedError


class SignupController(BaseSignupController):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create_user(self, create_data: schemas.RegistrationSchema):
        try:
            query = select(models.User).where(models.User.username == create_data.username)
            existing_user = await self.db.scalar(query)

            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь уже зарегистрирован."
                )
            else:
                hashed_password = pwd_context.hash(create_data.password)

                user = models.User(
                    username=create_data.username,
                    email=create_data.email,
                    password=hashed_password,
                    phone=create_data.phone
                )

                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)

            return JSONResponse(
                status_code=200,
                content={"detail": "Пользователь успешно зарегистрирован"}
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def send_confirmation_email(self, send_data: schemas.SendConfirmationEmailSchema):
        try:
            query = select(models.User).where(models.User.email == send_data.email)
            existing_email = await self.db.scalar(query)

            if existing_email:
                return "Сообщение отправлено на почту"

            else:
                raise HTTPException(
                    status_code=404,
                    detail="Проверьте правильность вводимой почты."
                )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    async def verify_confirmation_email(self, verify_data: schemas.VerifyConfirmationEmailSchema):
        try:
            query = select(models.User).where(models.User.email == verify_data.email)
            existing_user = await self.db.scalar(query)

            if existing_user:
                existing_user.is_verified = True

                await self.db.commit()

            else:
                raise HTTPException(
                    status_code=404,
                    detail="Проверьте правильность вводимой почты."
                )

            return JSONResponse(
                status_code=200,
                content={"detail": "Пользователь успешно верифицирован."}
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
