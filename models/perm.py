import datetime

import asyncer
from pydantic import BaseModel

from utils.auth.base import abac_enforcer

from .user import User


class PERMEnvironmentAttrs(BaseModel):
    time: datetime.datetime = datetime.datetime.now()


class PERMSub(BaseModel):
    user: User
    env: PERMEnvironmentAttrs = PERMEnvironmentAttrs()


class PERMRequest(BaseModel):
    sub: PERMSub
    obj: str
    act: str

    async def enforce(self):
        result = await asyncer.asyncify(abac_enforcer.enforce)(self.sub.model_dump(), self.obj, self.act)

        return result


class PERMPolicy(BaseModel):
    sub_rule: str
    obj: str
    act: str
