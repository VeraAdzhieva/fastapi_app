from pydantic import BaseModel
from src.domain.models.role import Subject


class PermissionDTO(BaseModel):
    object: str
    action: str

class RoleDTO(BaseModel):
    name: str
    permissions: list[PermissionDTO] = []

class UserInfo(BaseModel, Subject):
    username: str
    firstname: str
    lastname: str
