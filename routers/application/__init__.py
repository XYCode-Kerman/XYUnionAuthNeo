from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models import Application, User
from utils import applicationcol
from utils.auth import require_permission

router = APIRouter(prefix='/application', tags=['应用管理'])


@router.get(
    '/',
    response_model=List[Application],
    dependencies=[Depends(require_permission(
        'xyunionauth.application', 'read'))],
    name='获取应用列表',
    description='获取应用列表，需要`xyunionauth.application` 的 `read` 权限'
)
async def get_applications():
    return await applicationcol.find().to_list(None)


@router.get(
    '/{app_name}',
    response_model=Application,
    dependencies=[Depends(require_permission(
        'xyunionauth.application', 'read'))],
    name='获取应用信息',
    description='获取应用信息，需要 `xyunionauth.application` 的 `read` 权限'
)
async def get_application(app_name: str):
    return await applicationcol.find_one({'name': app_name})


@router.get(
    '/token/{app_name}',
    responses={
        200: {
            'description': '获取应用 token 成功',
            'content': {'application/json': {'example': {"token": "hello"}}}
        }
    },
    dependencies=[Depends(require_permission(
        'xyunionauth.application.token', 'read'))],
    name='获取应用 token',
    description='获取应用 token，需要 `xyunionauth.application.token` 的 `read` 权限'
)
async def get_application_token(app_name: str):
    app_doc = await applicationcol.find_one({'name': app_name})
    if app_doc is None:
        raise HTTPException(status_code=404, detail='应用不存在')

    app = Application(**app_doc)
    return {
        'token': app.token()
    }


@router.post(
    '/',
    response_model=Application,
    dependencies=[Depends(require_permission(
        'xyunionauth.application', 'write'))],
    name='创建应用',
    description='创建应用，需要 `xyunionauth.application` 的 `write` 权限'
)
async def create_application(application: Application):
    app = Application(**application.dict())

    # 检查是否存在
    if await applicationcol.find_one({'name': app.name}):
        raise HTTPException(status_code=400, detail='应用已存在')

    inserted = await applicationcol.insert_one(app.model_dump())

    return await applicationcol.find_one({'_id': inserted.inserted_id})
