from __future__ import annotations

from pwdlib import PasswordHash
from .models.user import User, UserAggregate

password_hash = PasswordHash.recommended()


class UserFactory:
    @staticmethod
    def create(username: str, password: str, firstname: str, lastname: str, roles: list[str] = None) -> UserAggregate:
        hash_password=password_hash.hash(password)
        username_lower = username.lower()

        if "admin" in username_lower:
            roles = ["Admin", "User"]
        elif "analyst" in username_lower or "analytics" in username_lower:
            roles = ["Analyst", "User"]
        else:
            roles = ["User"]

        entity = User(username=username, password=hash_password, firstname=firstname, lastname=lastname, roles=roles)
        return UserAggregate(root=entity)
