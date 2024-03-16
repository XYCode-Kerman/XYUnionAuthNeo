import datetime
import hashlib
from typing import Union

import jwt
import orjson
import simpleeval
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie, APIKeyHeader

from config import JWT_SECRET
from models import Action, CasbinRequest, Resource, Token, User
from models.application import Application
from models.casbin import CasbinSub
from utils import applicationcol, enforcer, resourcescol, usercol

router = APIRouter(prefix='/user', tags=['用户'])
apikey_scheme = APIKeyCookie(name='api-key', auto_error=False)


@router.post('/login', name='用户登录', description='> 注意：仅传入的 username 和 password 有效', response_model=Token)
async def handle_login(user: User):
    result = await usercol.find_one({'username': user.username, 'password': hashlib.sha1(user.password.encode('utf-8')).hexdigest()})
    if result is None:
        raise HTTPException(
            status_code=401,
            detail='用户名或密码错误'
        )

    token = Token(user=user, exp=int((datetime.datetime.now() +
                  datetime.timedelta(days=7)).timestamp()))
    token.token = jwt.encode(token.model_dump(mode='json'), JWT_SECRET)

    return token


@router.post('/register', name='注册用户', response_model=User)
async def handle_register(user: User):
    user.password = hashlib.sha1(user.password.encode('utf-8')).hexdigest()
    inserted = await usercol.insert_one(user.model_dump())
    user = await usercol.find_one({'_id': inserted.inserted_id})
    return user


@router.get('/token/check', name='检测 Token 有效', response_model=Union[User, Application])
async def check_token(token: str = Depends(apikey_scheme)) -> Union[User, Application]:
    try:
        token_decode: dict = jwt.decode(
            token, JWT_SECRET, algorithms=['HS256'])
        if token_decode.get('application', None) is None:
            token_decode: Token = Token(**token_decode)

            user = await usercol.find_one({'username': token_decode.user.username})
            return User(**user)
        else:
            token_decode: Application = Application(**token_decode)

            application = await applicationcol.find_one({'name': token_decode.application.name})
            return Application(**application)
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail='签名错误')
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail='令牌错误')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='令牌过期')


@router.get('/permission/check', name='检测权限', responses={
    200: {
        'content': {
            'application/json': {
                'example': {
                    'result': True
                }
            }
        }
    },
    403: {
        'description': '没有权限',
        'content': {
            'application/json': {
                'example': {
                    'detail': '无权限'
                }
            }
        }
    }
})
async def check_permission(resource: str, action: Action, user: Union[User, Application] = Depends(check_token)):
    request = CasbinRequest(
        sub=CasbinSub(user=user),
        resource=resource,
        action=action
    )

    try:
        result = enforcer.enforce(
            request.sub.model_dump(),
            request.resource,
            request.action.value
        )
    except simpleeval.AttributeDoesNotExist:
        pass

    if not result:
        raise HTTPException(status_code=403, detail='无权限')

    return {
        'result': result
    }
