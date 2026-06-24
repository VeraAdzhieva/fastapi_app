from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.domain.models.role import Action, Object, Subject
from src.infrastructure.auth.dependencies import CurrentUser
from src.infrastructure.auth.model import UserInfo

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/admin", summary="Настройки", tags=["Admin"])
async def get_settings(user: CurrentUser) -> dict[str, str]:
    authorized = UserInfo.check_permission(user, Object.INFO, Action.INFO)
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="Нет прав доступа",
        )
    return {
        "message": "Время дейсвтия токена пользователя: 60мин, пользователь может узнать о вероятности наличия диабета."
    }
