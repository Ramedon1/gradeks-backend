from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from web.depends.access_token import current_user_id
from web.methods.get_user_info import get_grades_by_period
from web.models.users.user import DistributionInfo, GradesInfo

distribution_router = APIRouter(prefix="/distribution", tags=["distribution"])


@distribution_router.post("/{distribution_type}/activate")
async def activate(
    user_id: Annotated[str, Depends(current_user_id)], distribution_type: str
) -> DistributionInfo:
    return
