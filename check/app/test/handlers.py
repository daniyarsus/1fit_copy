from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()


# Эмуляция проверки пользователя и его роли
def authenticate_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token"))):
    # Декодирование JWT токена
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "123", algorithms=["HS256"])
        username: str = payload.get("username")
        role: int = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Проверка роли пользователя
    if role != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return username


@router.get("/protected")
def get_protected_resource(username: str = Depends(authenticate_user)):
    return {"message": f"Welcome, {username}! You have access to this protected resource."}


@router.post("/check-protected-endpoint")
def check_protected_endpoint(token: str):
    import requests

    # Заголовок запроса с токеном JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # URL защищенного эндпоинта
    url = "http://127.0.0.1:8000/protected"

    # Отправка запроса GET к защищенному эндпоинту с использованием токена JWT
    response = requests.get(url, headers=headers)
    #body = {"key": "value"}
    #requests.post(url, headers=headers, json=body)

    # Обработка ответа
    if response.status_code == 200:
        return ("Запрос успешно выполнен! Ответ сервера:",
                response.json())
    else:
        return ("Ошибка при выполнении запроса:",
                response.status_code)
