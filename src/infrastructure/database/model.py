from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.infrastructure.database.db import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class UsersDBModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, nullable=True)
    roles = relationship("RoleDBModel", secondary="user_roles", back_populates="users")


class RoleDBModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    permissions = relationship(
        "PermissionDBModel", secondary="role_permissions", back_populates="roles"
    )
    users = relationship("UsersDBModel", secondary="user_roles", back_populates="roles")


class PermissionDBModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    object = Column(String, nullable=False)
    action = Column(String, nullable=False)

    roles = relationship(
        "RoleDBModel", secondary="role_permissions", back_populates="permissions"
    )
