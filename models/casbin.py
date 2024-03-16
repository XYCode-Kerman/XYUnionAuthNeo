import datetime
from typing import Optional, Union

from pydantic import BaseModel

from models.application import Application
from models.resources import Action, Resource
from models.user import User


class CasbinEnvironment(BaseModel):
    time: datetime.datetime = datetime.datetime.now()


class CasbinSub(BaseModel):
    user: Optional[Union[User, Application]] = None
    environment: CasbinEnvironment = CasbinEnvironment()


class CasbinRequest(BaseModel):
    sub: CasbinSub
    resource: str
    action: Action
