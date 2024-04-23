import datetime

import fastapi
from fastapi import APIRouter, Depends, HTTPException

from utils import db
from utils.auth import gen_application_token, hash_password
from utils.dependencies import require_application, require_permission

router = APIRouter(prefix='/application', tags=['应用管理'])


@router.post('/token/new', description="""创建Token。需要资源 `/application/token` 的 `new` 权限。

**注意**：请保存好 `app_id` 和 `app_secret`，它们是您应用的唯一标识，丢失此标识将无法正常使用该 Token。

**注意**：如密钥泄露，请立即将其 `reset`。""", responses={
    200: {
        'description': '成功获取Token',
        'content': {
            'application/json': {
                'example': {
                    'token': '生成的Token'
                }
            }
        }
    }
})
async def gen_token(app_id: str, app_secret: str, expries: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=7), user=Depends(require_permission('/application/token', 'new'))):
    token = gen_application_token(app_id, app_secret, exp=expries)

    await db.hset('xyuan_application_tokens', f'{app_id}_{hash_password(app_secret)}', token)

    return {
        'token': token
    }


@router.post('/token/reset', description='使得 Token 失效。', responses={
    200: {
        'description': '成功重置Token',
        'content': {
            'application/json': {
                'example': {
                    'message': 'Token已失效'
                }
            }
        }
    }
})
async def reset_token(app=Depends(require_application)):
    app_id = app[0]
    app_secret = app[1]

    await db.hdel('xyuan_application_tokens', f'{app_id}_{hash_password(app_secret)}')

    return {
        'message': 'Token已失效'
    }
