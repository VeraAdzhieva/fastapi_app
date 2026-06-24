import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

ALGORITHM = "HS256"

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN = 60


class TokenService:
    def create_access_token(self, data: dict[str, Any]) -> str:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN)

        payload = {
            **data,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }

        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
