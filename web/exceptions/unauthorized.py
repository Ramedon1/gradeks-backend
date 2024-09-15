from fastapi import HTTPException
from starlette import status

NoAccessTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bearer token is missing",
    headers={"WWW-Authenticate": "Bearer"},
)


AccessTokenNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token not found",
    headers={"WWW-Authenticate": "Bearer"},
)
