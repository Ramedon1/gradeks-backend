from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.users_grades import Users_grades
from db.models.users_grades_finally import Users_grades_finally


class DbManagerUsers(DbManagerBase):
    async def get_grades(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> list[Users_grades]:
        async with self.session_manager(outer_session) as session:
            statement = select(Users_grades).where(Users_grades.user_id == user_id)
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_period(
        self,
        user_id: str | UUID,
        start_date: datetime | str,
        end_date: datetime | str,
        outer_session: AsyncSession | None = None,
    ) -> list[Users_grades]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Users_grades)
                .where(Users_grades.user_id == user_id)
                .where(Users_grades.grading_date >= start_date)
                .where(Users_grades.grading_date <= end_date)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_subject(
        self, user_id: str | UUID, subject: str
    ) -> list[Users_grades]:
        async with self.session_manager() as session:
            statement = (
                select(Users_grades)
                .where(Users_grades.user_id == user_id)
                .where(Users_grades.subject == subject)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_quarter(
        self, user_id: str | UUID, quarter: str
    ) -> list[Users_grades_finally]:
        async with self.session_manager() as session:
            statement = (
                select(Users_grades_finally)
                .where(Users_grades_finally.user_id == user_id)
                .where(Users_grades_finally.quarter == quarter)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades
