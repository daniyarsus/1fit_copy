from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt

from fastapi import APIRouter, Depends, HTTPException, status

from auth.settings.config import settings


router = APIRouter()


@router.post("/jwt-create")
# Функция для создания JWT токена с ролью в виде целого числа и именем пользователя
def create_jwt_token(username: str, role: int, expires_delta: Union[timedelta, int] = 1800):
    # Определите ваш секретный ключ
    SECRET_KEY = settings.jwt_config.SECRET_KEY
    # Определите алгоритм шифрования
    ALGORITHM = "HS256"
    # Преобразуйте expires_delta в timedelta, если он представлен в секундах
    if isinstance(expires_delta, int):
        expires_delta = timedelta(seconds=expires_delta)
    # Определите время истечения токена
    expire = datetime.utcnow() + expires_delta
    # Подготовьте данные для токена
    to_encode = {"username": username, "role": role, "exp": expire}
    # Подпишите и верните токен
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
