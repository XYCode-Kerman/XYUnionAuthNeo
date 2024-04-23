import uuid
from typing import *

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID

    username: str
    password: str
    role: str
    user_attrs: Dict[str, Any] = {}
