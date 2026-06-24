from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from .role import Role

# =============================================================================
# VALUE OBJECTS (VO)
# =============================================================================


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) > 50:
            raise ValueError("Ошибка. Имя превышает 50 символов")
        elif len(self.value) < 3:
            raise ValueError("Ошибка.Придумайте логин более 3 символов")


# =============================================================================
# ENTITY
# =============================================================================


class User:
    """
    Сущность пользователя.
    """

    def __init__(
        self,
        username: Username,
        password: str,
        firstname: str,
        lastname: str,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        roles: Optional[List[Role]] = None,
    ) -> None:
        self.id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.created_at = created_at or datetime.now()
        self.last_login = last_login
        self.roles = self._convert_roles(roles or [])

    def _convert_roles(self, roles: list[Role]) -> list[Role]:
        converted = []
        for role in roles:
            if isinstance(role, str):
                converted.append(Role(name=role, permissions=[]))
            else:
                converted.append(role)

        return converted


# =============================================================================
# AGGREGATE
# =============================================================================


class UserAggregate:
    def __init__(self, root: User) -> None:
        self._root = root
        self.events: List[Any] = []

    @property
    def root(self) -> User:
        return self._root
