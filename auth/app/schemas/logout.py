from typing import Annotated

from pydantic import BaseModel


class LogoutSchema(BaseModel):
    jwt: Annotated[str, None]

