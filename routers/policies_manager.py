import datetime
from typing import *

import fastapi
from fastapi import APIRouter, Depends, HTTPException

from utils import db
from utils.auth import abac_enforcer, gen_application_token, hash_password
from utils.dependencies import require_application, require_permission

router = APIRouter(prefix='/policies', tags=['权限策略'])
Policy = Tuple[str, str, str]


@router.get('/', name='获取权限策略', response_model=List[Policy])
async def get_policies(application: str = Depends(require_application)):
    return abac_enforcer.get_policy()


@router.post('/', name='添加权限策略', response_model=bool)
async def add_policy(policy: Policy, application: str = Depends(require_application)):
    return abac_enforcer.add_policy(*policy)


@router.put('/', name='更新权限策略', response_model=bool)
async def update_policy(old: Policy, new: Policy, application: str = Depends(require_application)):
    return abac_enforcer.update_policy(old, new)


@router.delete('/', name='删除权限策略', response_model=bool)
async def delete_policy(policy: Policy, application: str = Depends(require_application)):
    return abac_enforcer.remove_policy(*policy)
