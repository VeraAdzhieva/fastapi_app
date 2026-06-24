from __future__ import annotations

from pwdlib import PasswordHash

from .models.role import Role
from .models.user import User, UserAggregate, Username

password_hash = PasswordHash.recommended()


class UserFactory:
    @staticmethod
    def create(
        username: Username,
        password: str,
        firstname: str,
        lastname: str,
        roles: list[Role],
    ) -> UserAggregate:
        hash_password = password_hash.hash(password)
        username_lower = username.value.lower()

        if "admin" in username_lower:
            roles = [Role(name="Admin"), Role(name="User")]
        elif "analyst" in username_lower or "analytics" in username_lower:
            roles = [Role(name="Analyst"), Role(name="User")]
        else:
            roles = [Role(name="User")]

        entity = User(
            username=username,
            password=hash_password,
            firstname=firstname,
            lastname=lastname,
            roles=roles,
        )
        return UserAggregate(root=entity)
