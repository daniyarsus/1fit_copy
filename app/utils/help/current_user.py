from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.settings.config import settings


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.jwt_config.SECRET_KEY, algorithms=[settings.jwt_config.ALGORITHM])
        id: int = payload.get('id')
        username: str = payload.get('username')
        email: str = payload.get('email')
        phone: int = payload.get('phone')

        return {
            'id': id,
            'username': username,
            'email': email,
            'phone': phone
        }

    except JWTError:
        pass
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
