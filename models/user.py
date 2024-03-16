from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from models.base import BsonObjectId


class User(BaseModel):
    _id: Optional[BsonObjectId] = None
    username: str
    email: str
    password: str
    role: str = 'default'
    application_addtional_data: Dict[str, Any]


class Token(BaseModel):
    token: Optional[str] = None
    user: User
    exp: Union[datetime, int]
