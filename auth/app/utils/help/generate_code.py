from random import randint
from fastapi import HTTPException


def generate_verification_code() -> int:
    try:
        code = randint(100000, 999999)
        return code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
