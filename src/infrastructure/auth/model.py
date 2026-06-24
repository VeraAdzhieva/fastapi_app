from pydantic import BaseModel

from src.domain.models.role import Subject


class UserInfo(BaseModel, Subject):
    username: str
    firstname: str
    lastname: str
