from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.domain.models.role import Action, Object, Permission, Role
from src.domain.models.user import User, UserAggregate
from src.domain.repository import UsersRepository
from src.infrastructure.database.model import RoleDBModel, UsersDBModel


class SqlAlchemyUsersRepository(UsersRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, username: str) -> Optional[UserAggregate]:
        """
        Получает пользователя по username.
        """
        db_model = self.session.query(UsersDBModel).filter_by(username=username).first()
        if not db_model:
            return None

        roles = []
        for db_role in db_model.roles:
            permissions = [
                Permission(object=Object(p.object), action=Action(p.action))
                for p in db_role.permissions
            ]
            roles.append(Role(name=db_role.name, permissions=permissions))

        root_entity = User(
            username=db_model.username,
            password=db_model.password,
            firstname=db_model.firstname,
            lastname=db_model.lastname,
            roles=roles,
        )

        return UserAggregate(root=root_entity)

    def add(self, user_agg: UserAggregate) -> None:
        """
        Добавляет нового пользователя.
        """
        root = user_agg.root

        role_names = [
            role.name if hasattr(role, "name") else role for role in root.roles
        ]
        db_roles = (
            self.session.query(RoleDBModel)
            .filter(RoleDBModel.name.in_(role_names))
            .all()
        )

        db_model = UsersDBModel(
            username=root.username,
            password=root.password,
            firstname=root.firstname,
            lastname=root.lastname,
            created_at=root.created_at,
            last_login=root.last_login,
            roles=db_roles,
        )

        self.session.add(db_model)

    def save(self, user_agg: UserAggregate) -> None:
        """
        Сохраняет изменения.
        """
        root = user_agg.root
        db_model = self.session.query(UsersDBModel).filter_by(user_id=root.id).first()

        if not db_model:
            raise ValueError("Пользователь не найден")

        db_model.username = root.username
        db_model.password = root.password
        db_model.firstname = root.firstname
        db_model.lastname = root.lastname
        db_model.created_at = root.created_at
        db_model.last_login = root.last_login
