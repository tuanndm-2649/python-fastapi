from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from demo_fastapi.constants.auth import TOKEN_URL
from demo_fastapi.constants.message import (
    INVALID_TOKEN,
    USER_INACTIVE,
)
from demo_fastapi.core.security import decode_access_token
from demo_fastapi.crud.users import retrieve_user
from demo_fastapi.database import get_db
from demo_fastapi.exceptions import ForbiddenException, UnauthorizedException
from demo_fastapi.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    user_id = decode_access_token(token)

    if user_id is None:
        raise UnauthorizedException(INVALID_TOKEN)

    user = retrieve_user(db, user_id)

    if user is None:
        raise UnauthorizedException(INVALID_TOKEN)

    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise ForbiddenException(USER_INACTIVE)

    return user
