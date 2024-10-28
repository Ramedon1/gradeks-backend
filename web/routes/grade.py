from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from db.manager import db_manager
from web.depends.access_token import current_user_id
from web.exceptions.grades import GradeTypeException
from web.models.users.user import GradeType, NewGrade

grade_router = APIRouter(prefix="/grade", tags=["grade"])


@grade_router.get("/new")
async def new(user_id: Annotated[str, Depends(current_user_id)]) -> list[NewGrade]:
    new_grades = await db_manager.new_grades.get_new_grades_by_user(user_id)
    return [NewGrade.model_validate(item, from_attributes=True) for item in new_grades]


@grade_router.post("/change/{grade_type}")
async def new_type_grade(
    user_id: Annotated[str, Depends(current_user_id)], grade_type: str
) -> GradeType:
    if grade_type not in ["old", "new"]:
        raise GradeTypeException

    new_grade_type = await db_manager.users.change_grade_type(user_id, grade_type)
    return GradeType(grade_type=new_grade_type)


@grade_router.post("/finally")
async def finally_grades():
    pass
    # TODO: Потом сделать итоговые оценки за четвери и годовые
