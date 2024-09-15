from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from web.depends.access_token import current_user_id
from web.methods.get_user_info import get_grades_by_period
from web.models.users.user import GradesInfo

grade_router = APIRouter(prefix="/grade", tags=["grade"])


@grade_router.post("/me")
async def me(
    user_id: Annotated[str, Depends(current_user_id)],
    start_date: datetime,
    end_date: datetime,
) -> list[GradesInfo]:
    return await get_grades_by_period(user_id, start_date, end_date)


@grade_router.post("/finally")
async def finally_grades():
    pass
    # TODO: Потом сделать итоговые оценки за четвери и годовые
