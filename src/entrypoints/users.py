
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.application.commands import Register, LoginIn
from src.application.handlers import (
    RegisterHandler,
    AuthHandler,
)
from src.infrastructure.database.db import SessionLocal
from src.infrastructure.database.uow import SqlAlchemyUnitOfWork
from src.infrastructure.auth.token_service import TokenService, ACCESS_TOKEN
from src.infrastructure.auth.model import UserInfo
from src.infrastructure.auth.dependencies import CurrentUser

from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])

class RegisterDTO(BaseModel):
    username: str = Field(..., description="Логин пользователя", min_length=3, max_length=50)
    password: str = Field(..., description="Пароль", min_length=6, max_length=50)
    firstname: str = Field(..., description="Имя", max_length=50)
    lastname: str = Field(..., description="Фамилия", max_length=50)

class LoginInDTO(BaseModel):
    username: str = Field(..., description="Имя пользователя", min_length=3, max_length=50)
    password: str = Field(..., description="Пароль", min_length=6, max_length=50)


@router.post("/registration", summary="Регистрация пользователя", tags=["Users"])
def registration(user: RegisterDTO) -> dict[str, str]:
    with SqlAlchemyUnitOfWork(SessionLocal) as uow:
        handler = RegisterHandler(uow)
        cmd = Register(**user.dict())
        try:
            handler(cmd)
            return {"message": f"Пользователь {user.username} зарегистрирован."}
        except Exception as e:
            return {"message": str(e)}
        

@router.post("/auth", summary="Авторизация", tags=["Users"])
def authenticate(login: LoginInDTO) -> dict[str, str]:
    with SqlAlchemyUnitOfWork(SessionLocal) as uow:
        handler = AuthHandler(uow, TokenService())
        cmd = LoginIn(**login.dict())
        try:
            token = handler(cmd)
            return {"message": f"Пользователь {login.username} авторизован. Токен: {token}Время действия: {ACCESS_TOKEN}"}
        except Exception as e:
            return {"message": str(e)}
        

@router.get("/me", summary="Получить данные авторизованного пользовтаеля")
async def me(
    user_model: CurrentUser
) -> UserInfo:
    return UserInfo(
        username=user_model.username,
        firstname=user_model.firstname,
        lastname=user_model.lastname,
        roles=user_model.roles,
    )
