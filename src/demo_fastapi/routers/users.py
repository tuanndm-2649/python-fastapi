from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from demo_fastapi.common.validators import get_user_profile
from demo_fastapi.constants.auth import PASSWORD_MAX_LENGTH
from demo_fastapi.constants.message import (
    EMAIL_ALREADY_EXISTS,
    EMAIL_OR_USERNAME_ALREADY_EXISTS,
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    USER_NOT_FOUND,
    USERNAME_ALREADY_EXISTS,
)
from demo_fastapi.core.security import create_access_token, verify_password
from demo_fastapi.crud.users import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
    update_user,
)
from demo_fastapi.database import get_db
from demo_fastapi.dependencies.auth import get_current_user
from demo_fastapi.exceptions import ConflictException, UnauthorizedException
from demo_fastapi.models import User
from demo_fastapi.schemas.auth import Token
from demo_fastapi.schemas.pagination import PageResponse, PaginationParams
from demo_fastapi.schemas.responses import (
    UserProfileResponse,
    error_response,
    not_found_response,
)
from demo_fastapi.schemas.users import (
    UserPublicResponse,
    UserRegister,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "", response_model=PageResponse[UserPublicResponse], summary="Get list users"
)
def list_users(
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Query()],
) -> PageResponse[UserPublicResponse]:
    return get_users(db, pagination)


@router.get(
    "/{username}/profile",
    response_model=UserProfileResponse,
    summary="User profile",
    responses=not_found_response(USER_NOT_FOUND),
)
def user_profile(
    username: str,
    db: Annotated[Session, Depends(get_db)],
) -> UserProfileResponse:
    user = get_user_profile(db, username)

    return UserProfileResponse.model_validate(user)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    responses=error_response(
        status.HTTP_409_CONFLICT, EMAIL_OR_USERNAME_ALREADY_EXISTS
    ),
)
def user_register(
    payload: UserRegister, db: Annotated[Session, Depends(get_db)]
) -> User:
    if get_user_by_email(db, payload.email) is not None:
        raise ConflictException(EMAIL_ALREADY_EXISTS)

    if get_user_by_username(db, payload.username) is not None:
        raise ConflictException(USERNAME_ALREADY_EXISTS)

    try:
        return create_user(db, payload)
    except IntegrityError:
        raise ConflictException(EMAIL_OR_USERNAME_ALREADY_EXISTS)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    responses=error_response(status.HTTP_401_UNAUTHORIZED, INVALID_CREDENTIALS),
)
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form(max_length=PASSWORD_MAX_LENGTH)],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = get_user_by_username(db, username)

    if user is None or not verify_password(password, user.hashed_password):
        raise UnauthorizedException(INVALID_CREDENTIALS)

    return Token(access_token=create_access_token(user.id))


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current user",
    responses=error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
)
def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    responses=error_response(status.HTTP_401_UNAUTHORIZED, INVALID_TOKEN),
)
def update_me(
    payload: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return update_user(db, current_user, payload)
