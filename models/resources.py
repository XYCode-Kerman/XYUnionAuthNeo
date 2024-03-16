from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from models.application import Application


class Action(str, Enum):
    read = 'read'
    write = 'write'
    delete = 'delete'
    all = 'all'


class Resource(BaseModel):
    application: Application
    resource_id: str
    allow_actions: List[Action] = []
    description: Optional[str] = None

    @property
    def resource_id_with_namespace(self):
        return f'{self.application.name}.{self.resource_id}'
