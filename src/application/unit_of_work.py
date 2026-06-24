from __future__ import annotations
from typing import Optional, Protocol, Type
from types import TracebackType
from src.domain.repository import UsersRepository


class UnitOfWork(Protocol):
    users: UsersRepository

    def __enter__(self) -> "UnitOfWork":
        pass

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
