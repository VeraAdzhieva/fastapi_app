from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class Role(BaseModel):
    name: str
    permissions: list[Permission]


class Permission(BaseModel):
    object: Object
    action: Action


class Action(str, Enum):
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"
    INFO = "info"
    PREDICT = "predict"


class Object(str, Enum):
    USER = "user"
    INFO = "info"


@dataclass
class Subject:
    roles: list[Role]

    def check_permission(subject: Subject, object_: Object, action: Action) -> bool:
        for role in subject.roles:
            for permission in role.permissions:
                if permission.object == object_ and permission.action == action:
                    return True
        return False
