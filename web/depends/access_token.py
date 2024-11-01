from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from rediska import redis_manager
from web.exceptions.unauthorized import (
    AccessTokenNotFoundException,
    NoAccessTokenException,
)


async def current_user_id(
    authorization: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer())
    ],
) -> str:
    if not authorization.scheme == "Bearer":
        raise NoAccessTokenException

    user_id = await redis_manager.access_tokens.get_user_id_by_access_token(
        authorization.credentials
    )
    if user_id is None:
        raise AccessTokenNotFoundException

    return user_id
