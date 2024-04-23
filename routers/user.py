import uuid
from typing import *

import fastapi
from fastapi import APIRouter, Body, Depends, HTTPException

from models import User
from utils import db
from utils.auth import gen_token, hash_password
from utils.dependencies import require_permission, require_user

router = APIRouter(prefix='/user', tags=['用户管理'])


@router.post('/register', name='用户注册', response_model=User)
async def register(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    if await db.hget('xyuan_users', username) is not None:
        raise HTTPException(status_code=400, detail='用户名已存在')

    user = User(id=uuid.uuid4(), username=username,
                password=hash_password(password), role='default')

    await db.hset('xyuan_users', username, user.model_dump_json())

    return User.model_validate_json(await db.hget('xyuan_users', username))


@router.post('/login', name='用户登录', responses={
    200: {
        'description': '登录成功',
        'content': {
            'application/json': {
                'example': {
                    'token': 'jwt_token'
                }
            }
        }
    }
})
async def login(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    if await db.hget('xyuan_users', username) is None:
        raise HTTPException(status_code=400, detail='用户不存在')

    user = User.model_validate_json(await db.hget('xyuan_users', username))

    if hash_password(password) != user.password:
        raise HTTPException(status_code=400, detail='密码错误')

    return {
        'token': gen_token(user)
    }


@router.get('/me', name='获取当前用户信息', response_model=User, description='需要资源 `/user/me` 的 `read` 权限')
async def get_me(user: User = Depends(require_permission('/user/me', 'read'))):
    return user


@router.get('/check/permission', name='检查是否有权限', response_model=User)
async def check_permission(resource: str, action: str, user: User = Depends(require_user)):
    func = require_permission(resource, action)

    return await func(user)
