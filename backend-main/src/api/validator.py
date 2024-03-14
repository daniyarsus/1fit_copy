from fastapi import HTTPException


def validate_user_admin(user_role_id, roles: list):
    if user_role_id not in roles:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return True


