from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.new_grades import NewGrades
from web.models.users.user import NewGrade


class DbManagerNewGrades(DbManagerBase):
    async def get_new_grades_by_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> list[NewGrade]:
        async with self.session_manager(outer_session) as session:
            statement = select(NewGrades).where(NewGrades.user_id == user_id)
            result = await session.exec(statement)
            grades = result.all()

            return [
                NewGrade(
                    grade=grade.grade,
                    old_grade=grade.grade_old,
                    date=str(grade.grading_date.strftime("%d.%m")),
                    subject=grade.subject,
                    coff=grade.grade_weight,
                )
                for grade in grades
            ]
