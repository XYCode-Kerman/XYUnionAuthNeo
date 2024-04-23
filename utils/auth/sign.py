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


def gen_user_token(user: User, exp: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=7)) -> str:
    return jwt.encode(
        {
            **user.model_dump(mode='json'),
            'exp': exp
        },
        SECRET
    )


def gen_application_token(app_id: str, app_secret: str, exp: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=7)) -> str:
    return jwt.encode(
        {
            'app_id': app_id,
            'app_secret': app_secret,
            'exp': exp
        },
        SECRET
    )
