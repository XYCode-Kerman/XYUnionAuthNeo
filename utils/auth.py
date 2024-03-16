from fastapi import Depends

from models.resources import Action
from models.user import User
from routers.user import check_permission, check_token


def require_permission(resource: str, action: Action):
    async def wrapper(user: User = Depends(check_token)):
        return await check_permission(resource, action, user)

    return wrapper
