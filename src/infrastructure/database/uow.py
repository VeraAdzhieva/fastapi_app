from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker
from types import TracebackType
from typing import Optional, Type
from src.application.unit_of_work import UnitOfWork
from src.infrastructure.database.repositories import (
    SqlAlchemyUsersRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self.session = Session
        self.users = SqlAlchemyUsersRepository(self.session)

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.users = SqlAlchemyUsersRepository(self.session)
        return self
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()
