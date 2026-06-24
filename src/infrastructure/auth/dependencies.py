from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infrastructure.auth.token_service import ALGORITHM
from src.infrastructure.auth.model import UserInfo
import jwt, os

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def _get_user_info_from_token(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserInfo:
    """
    Достает из JWT токена данные о пользователе
    """
    auth_token = creds.credentials

    try:
        user_payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        return UserInfo(
            username=user_payload["username"],
            firstname=user_payload["firstname"],
            lastname=user_payload["lastname"],
            roles=user_payload["roles"],
        )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истёк",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Неверный токен {e}",
        )

CurrentUser = Annotated[UserInfo, Depends(_get_user_info_from_token)]