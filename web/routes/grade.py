from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from common.enums.periods import PeriodsEnum
from db.manager import db_manager
from web.depends.access_token import current_user_id
from web.exceptions.grades import GradeFilterTypeException, GradeTypeException
from web.methods.get_diary_info import get_diary_info
from web.models.users.user import DiaryInfo, GradeType, GradeTypeFilter

grade_router = APIRouter(prefix="/grade", tags=["grade"])


@grade_router.post("/change/{grade_type}")
async def new_type_grade(
    user_id: Annotated[str, Depends(current_user_id)], grade_type: str
) -> GradeType:
    if grade_type not in ["old", "new"]:
        raise GradeTypeException

    new_grade_type = await db_manager.users.change_grade_type(user_id, grade_type)
    return GradeType(grade_type=new_grade_type)


@grade_router.post("/get")
async def get_grades(
    user_id: Annotated[str, Depends(current_user_id)], request: GradeTypeFilter
) -> list[DiaryInfo]:
    if request.filter not in PeriodsEnum.__members__:
        raise GradeFilterTypeException
    return await get_diary_info(user_id, request.filter)


@grade_router.post("/finally")
async def finally_grades():
    pass
    # TODO: Потом сделать итоговые оценки за четвери и годовые
