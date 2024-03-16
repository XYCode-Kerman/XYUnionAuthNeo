from typing import Optional

import jwt
from pydantic import BaseModel

from config import JWT_SECRET


class Application(BaseModel):
    name: str
    description: str

    def token(self) -> str:
        return jwt.encode(
            {
                'application': self.name,
                'role': 'application'
            },
            JWT_SECRET,
            algorithm='HS256'
        )
