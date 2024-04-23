import datetime
import hashlib

import jwt

from configs import SECRET
from models.user import User


def hash_password(password: str) -> str:
    return hashlib.sha512(
        hashlib.sha1(password.encode() + SECRET.encode()
                     ).hexdigest().encode() + SECRET.encode()
    ).hexdigest()


def gen_token(user: User, exp: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=7)) -> str:
    return jwt.encode(
        {
            **user.model_dump(mode='json'),
            'exp': exp
        },
        SECRET
    )
