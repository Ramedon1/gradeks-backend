from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from db.manager import db_manager
from web.depends.access_token import current_user_id
from web.models.users.user import Distribution

distribution_router = APIRouter(prefix="/distribution", tags=["distribution"])


@distribution_router.post("/activate")
async def activate(user_id: Annotated[str, Depends(current_user_id)]) -> Distribution:
    try:
        await db_manager.distribution.activate_distribution(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Distribution(
        distribution_status=await db_manager.distribution.get_distribution_status_user(
            user_id=user_id
        )
    )


@distribution_router.post("/deactivate")
async def deactivate(user_id: Annotated[str, Depends(current_user_id)]) -> Distribution:
    try:
        await db_manager.distribution.deactivate_distribution(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Distribution(
        distribution_status=await db_manager.distribution.get_distribution_status_user(
            user_id=user_id
        )
    )
