from src.application.commands import Predict, Register, LoginIn
from src.infrastructure.ml.onnx_service import OnnxPredict
from src.application.unit_of_work import UnitOfWork
from fastapi import HTTPException
from src.domain.factory import UserFactory
from pwdlib import PasswordHash
from src.infrastructure.auth.token_service import TokenService
from src.infrastructure.auth.model import UserInfo
from src.domain.models.role import Object, Action

predictor = OnnxPredict()

password_hash = PasswordHash.recommended()



class PredictHandler:
    def __call__(self, cmd: Predict, user) -> float:
        """
        Вероятность диабета.
        """
        authorized = UserInfo.check_permission(user, Object.USER, Action.PREDICT)
        if not authorized:
            raise HTTPException(
                status_code=403,
                detail="Нет прав доступа",
            )
        features = cmd.to_features_array()
        result = predictor.predict(features)

        return result
    

class RegisterHandler:
    """
    Регистрация.
    """
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        

    def __call__(self, cmd: Register) -> None:
        """
        Регистрация.
        """
        if self.uow and self.uow.users:
            existUser = self.uow.users.get(cmd.username)

        if existUser:
            raise HTTPException(
                status_code=400,
                detail="Пользователь существует",
            )
        
        user_agg = UserFactory.create(cmd.username, cmd.password, cmd.firstname, cmd.lastname, roles=["user"])
        self.uow.users.add(user_agg)
        self.uow.commit()


class AuthHandler:
    """
    Аутентификация
    """
    def __init__(self, uow: UnitOfWork, token_service: TokenService):
        self.uow = uow
        self.token_service = token_service

    def __call__(self, cmd: LoginIn) -> None:
        if self.uow and self.uow.users:
            user_model = self.uow.users.get(cmd.username)

        if not user_model:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден",
            )
        
        user = user_model.root

        if not password_hash.verify(cmd.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )
        
        return self.token_service.create_access_token(
            {
                "username": user.username,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "roles": [role.model_dump() for role in user.roles],
            }
        )
