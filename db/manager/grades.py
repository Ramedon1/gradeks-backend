from datetime import date
from uuid import UUID

from sqlalchemy import update
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

    async def get_grades_by_subject(
        self,
        user_id: str | UUID,
        subject: str,
        outer_session: AsyncSession | None = None,
    ) -> list[Grades]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(Grades.subject == subject)
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def get_grades_by_quarter(
        self,
        user_id: str | UUID,
        period_date_start: date,
        period_date_end: date,
        outer_session: AsyncSession | None = None,
    ) -> list[Grades]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(
                    (Grades.grading_date >= period_date_start)
                    & (Grades.grading_date <= period_date_end)
                )
            )
            result = await session.exec(statement)
            grades = result.all()

            return grades

    async def add_grade(self, grade: Grades, outer_session: AsyncSession | None = None):
        async with self.session_manager(outer_session) as session:
            session.add(grade)
            await session.commit()
            await session.refresh(grade)

    async def change_grade(
        self,
        grade_id: str | UUID,
        new_grade: int,
        grade_weight: int,
        outer_session: AsyncSession | None = None,
    ):
        async with self.session_manager(outer_session) as session:
            statement = (
                update(Grades)
                .where(Grades.grade_id == grade_id)
                .values(grade=new_grade, grade_weight=grade_weight)
            )
            await session.exec(statement)
            await session.commit()

    async def exist_grade(
        self, grade: Grades, outer_session: AsyncSession | None = None
    ) -> Grades | None:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Grades)
                .where(Grades.subject == grade.subject)
                .where(Grades.grading_date == grade.grading_date)
            )
            result = await session.exec(statement)
            grade = result.first()

            return grade if grade else None

    async def get_grade_by_subject(
        self,
        user_id: str | UUID,
        subject: str,
        outer_session: AsyncSession | None = None,
    ) -> Grades:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(Grades)
                .where(Grades.user_id == user_id)
                .where(Grades.subject == subject)
            )
            result = await session.exec(statement)
            grade = result.all()

            return grade if grade else None

    async def delete_grade(
        self, grade_id: str | UUID, outer_session: AsyncSession | None = None
    ):
        async with self.session_manager(outer_session) as session:
            statement = select(Grades).where(Grades.grade_id == grade_id)
            result = await session.exec(statement)
            grade = result.first()

            if grade:
                await session.delete(grade)
                await session.commit()
            else:
                await session.rollback()

    async def delete_grades_by_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ):
        async with self.session_manager(outer_session) as session:
            statement = select(Grades).where(Grades.user_id == user_id)
            result = await session.exec(statement)
            grades = result.all()

            for grade in grades:
                await session.delete(grade)

            await session.commit()
