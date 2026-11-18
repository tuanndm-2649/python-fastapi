from datetime import UTC, datetime, timedelta
from uuid import UUID

import bcrypt
import jwt

from demo_fastapi.constants.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    PASSWORD_ENCODE_TYPE,
)
from demo_fastapi.core.config import SECRET_KEY


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(PASSWORD_ENCODE_TYPE), bcrypt.gensalt()
    ).decode(PASSWORD_ENCODE_TYPE)


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(PASSWORD_ENCODE_TYPE),
        hashed_password.encode(PASSWORD_ENCODE_TYPE),
    )


def create_access_token(user_id: UUID) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> UUID | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return UUID(payload["sub"])
    except jwt.InvalidTokenError:
        return None
