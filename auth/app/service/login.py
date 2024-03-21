from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException

from jose import jwt, JWTError

from app.repository.base import AbstractRepository

from app.schemas.login import LoginUsernameSchema, LoginEmailSchema, LoginPhoneSchema, UpdateRefreshTokenSchema

from app.settings.config import settings

from app.settings.redis.connection import redis_client_user


SECRET_KEY = settings.jwt_config.SECRET_KEY
ALGORITHM = settings.jwt_config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS


class LoginService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo = user_repo()

    @staticmethod
    async def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def _create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def _get_user_by_username(self, username: str):
        user = await self.user_repo.get_one(username=username)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанным именем не найден!"
            )
        return user

    async def _get_user_by_email(self, email: str):
        user = await self.user_repo.get_one(email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанной почтой не найден!"
            )
        return user

    async def _get_user_by_phone(self, phone: str):
        user = await self.user_repo.get_one(phone=phone)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанным телефоном не найден!"
            )
        return user

    async def login_by_username(self, data: LoginUsernameSchema):
        try:
            user = await self._get_user_by_username(data.username)

            if not user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь не подтвержден!"
                )

            if not user.password == data.password:
                raise HTTPException(
                    status_code=400,
                    detail="Неверный пароль!"
                )

            access_token = await self._create_access_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )
            refresh_token = await self._create_refresh_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )

            await redis_client_user.set(name=str(user.id),
                                        value=refresh_token,
                                        ex=settings.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS)

            return {"access_token": access_token, "refresh_token": refresh_token}

        except JWTError:
            pass
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def login_by_email(self, data: LoginEmailSchema):
        try:
            user = await self._get_user_by_email(data.email)

            if not user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь не подтвержден!"
                )

            if not user.password == data.password:
                raise HTTPException(status_code=400, detail="Неверный пароль!")

            access_token = await self._create_access_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )
            refresh_token = await self._create_refresh_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )

            await redis_client_user.set(name=str(user.id),
                                        value=refresh_token,
                                        ex=settings.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS)

            return {"access_token": access_token, "refresh_token": refresh_token}

        except JWTError:
            pass
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def login_by_phone(self, data: LoginPhoneSchema):
        try:
            user = await self._get_user_by_phone(data.phone)

            if not user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь не подтвержден!"
                )

            if not user.password == data.password:
                raise HTTPException(status_code=400, detail="Неверный пароль!")

            access_token = await self._create_access_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )
            refresh_token = await self._create_refresh_token(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone
                }
            )

            await redis_client_user.set(name=str(user.id),
                                        value=refresh_token,
                                        ex=settings.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS)

            return {"access_token": access_token, "refresh_token": refresh_token}

        except JWTError:
            pass
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def update_refresh_token(self, data: UpdateRefreshTokenSchema):
        try:
            decoded_token = jwt.decode(data.jwt,
                                       SECRET_KEY,
                                       algorithms=[ALGORITHM])

            user_id = decoded_token.get("id")
            if user_id:
                refresh_token = await redis_client_user.get(str(user_id))

                if refresh_token and refresh_token.decode("utf-8") == data.jwt:
                    new_refresh_token = await self._create_refresh_token(
                        data={
                            "id": user_id,
                            "username": decoded_token.get("username"),
                            "email": decoded_token.get("email"),
                            "phone": decoded_token.get("phone")
                        }
                    )

                    await redis_client_user.set(name=str(user_id),
                                                value=new_refresh_token,
                                                ex=settings.jwt_config.REFRESH_TOKEN_EXPIRE_DAYS
                                                )

                    return {"refresh_token": new_refresh_token}

        except JWTError:
            pass
        raise HTTPException(
            status_code=401,
            detail="Неверный токен!"
        )
