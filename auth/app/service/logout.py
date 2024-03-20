from datetime import datetime, timedelta

from typing import Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from jose import jwt, JWTError

from app.schemas.logout import LogoutSchema

from app.settings.redis.connection import redis_client_jwt

from app.settings.config import settings


class LogoutService:
    @staticmethod
    async def logout_user(data: LogoutSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            token = data.jwt
            token_ttl = int(timedelta(minutes=60).total_seconds())

            # Декодировать JWT и получить полезную нагрузку
            try:
                payload = jwt.decode(token, settings.jwt_config.SECRET_KEY, algorithms=["HS256"])
            except JWTError as e:
                raise HTTPException(
                    status_code=401,
                    detail=str(e)
                )

            username = payload["username"]
            # Добавить в Redis JWT в качестве ключа и имя пользователя в качестве значения
            await redis_client.set(name=token, value=username, ex=token_ttl)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        return JSONResponse(content={
            "message": "Пользователь успешно вышел из сессии!"
            }
        )
