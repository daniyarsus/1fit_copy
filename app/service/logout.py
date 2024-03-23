from datetime import datetime, timedelta

from typing import Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from jose import jwt, JWTError

from app.schemas.logout import LogoutSchema

from app.settings.redis.connection import redis_client_auth

from app.settings.config import settings


class LogoutService:
    @staticmethod
    async def logout_user(data: LogoutSchema) -> Optional[JSONResponse | HTTPException]:
        try:
            token = data.jwt

            # Декодировать JWT и получить полезную нагрузку
            try:
                payload = jwt.decode(token, settings.jwt_config.SECRET_KEY, algorithms=["HS256"])
            except JWTError as e:
                raise HTTPException(
                    status_code=401,
                    detail=str(e)
                )

            id = payload["id"]
            session_id = payload["session_id"]
            # Добавить в Redis JWT в качестве ключа и имя пользователя в качестве значения

            await redis_client_auth.delete(f"jwt_user_id:{id}_session_id:{session_id}")

            return JSONResponse(content={
                "message": "Пользователь успешно вышел из сессии!"
            }
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
