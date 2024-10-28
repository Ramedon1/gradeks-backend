from datetime import date, datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.grades import Grades


class DbManagerGrades(DbManagerBase):
    async def get_grades_by_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> list[Grades]:
        async with self.session_manager(outer_session) as session:
            statement = select(Grades).where(Grades.user_id == user_id)
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_period(
        self,
        user_id: str | UUID,
        start_date: datetime | str,
        end_date: datetime | str,
        outer_session: AsyncSession | None = None,
    ) -> list[Grades]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(Grades.grading_date >= start_date)
                .where(Grades.grading_date <= end_date)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_subject(
        self, user_id: str | UUID, subject: str
    ) -> list[Grades]:
        async with self.session_manager() as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(Grades.subject == subject)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_quarter(
        self, user_id: str | UUID, quarter_date_start: date, quarter_date_end: date
    ) -> list[Grades]:
        async with self.session_manager() as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(
                    (Grades.grading_date >= quarter_date_start)
                    & (Grades.grading_date <= quarter_date_end)
                )
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades
