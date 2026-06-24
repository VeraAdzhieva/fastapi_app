from __future__ import annotations

from typing import Optional, Protocol

from .models.user import UserAggregate


class UsersRepository(Protocol):
    def get(self, username: str) -> Optional[UserAggregate]:
        pass

    def save(self, user: UserAggregate) -> None:
        pass

    def add(self, user: UserAggregate) -> None:
        pass
