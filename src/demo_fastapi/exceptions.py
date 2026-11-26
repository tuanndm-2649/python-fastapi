from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UnauthorizedException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ConflictException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class ForbiddenException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )
