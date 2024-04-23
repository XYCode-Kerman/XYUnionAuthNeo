import jwt
import pydantic
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from configs import SECRET
from models import PERMRequest, PERMSub, User

apikey_schema = APIKeyHeader(
    name="X-XYUAN-Token", description='XYUAN 的 APIKEY，可以是用户 Token 或者其他。')


def require_user(apikey: str = Depends(apikey_schema)) -> User:
    try:
        decoded = jwt.decode(apikey, SECRET, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, '过期 Token')
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(401, '不合法 Token')
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(401, '不合法 Token')

    try:
        user = User.model_validate(decoded)
    except pydantic.ValidationError:
        raise HTTPException(401, '不合法 Token')

    return user


def require_permission(resource: str, action: str):
    async def wrapper(user: User = Depends(require_user)):
        request = PERMRequest(
            sub=PERMSub(
                user=user
            ),
            obj=resource,
            act=action
        )

        if not await request.enforce():
            raise HTTPException(403, '没有权限')

        return user

    return wrapper
