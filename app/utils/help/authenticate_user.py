from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.settings.config import settings
from app.settings.redis.connection import redis_client_auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/signin/token-username")


async def get_authenticate_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_config.SECRET_KEY, algorithms=["HS256"])
        id: str = payload.get("id")
        session_id: str = payload.get("session_id")
        if id is None or session_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Проверка наличия токена в Redis
    redis_token = await redis_client_auth.get(f"jwt_user_id:{id}_session_id:{session_id}")
    if not redis_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found in Redis",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
