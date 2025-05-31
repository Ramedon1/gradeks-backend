from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db.manager.base import DbManagerBase
from db.models.grades_finally import GradesFinally


class DbManagerGradesFinally(DbManagerBase):
    async def add_finally_grade(
        self,
        user_id: str | UUID,
        grade: int,
        subject: str,
        quarter: str,
        outer_session: AsyncSession | None = None,
    ) -> GradesFinally:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession
            new_finally_grade = GradesFinally(
                user_id=user_id, grade=grade, subject=subject, quarter=quarter
            )
            session.add(new_finally_grade)
            await session.commit()
            await session.refresh(new_finally_grade)
            return new_finally_grade

    async def get_finally_grades_by_user_id(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> list[GradesFinally]:
        async with self.session_manager(outer_session) as session:
            statement = select(GradesFinally).where(GradesFinally.user_id == user_id)
            result = await session.execute(statement)
            grades = result.scalars().all()
            return grades

    async def change_finally_grade(
        self,
        user_id: str | UUID,
        new_grade: int,
        subject: str,
        quarter: str,
        outer_session: AsyncSession | None = None,
    ) -> GradesFinally | None:
        async with self.session_manager(outer_session) as session:
            statement = (
                update(GradesFinally)
                .where(GradesFinally.user_id == user_id)
                .where(GradesFinally.subject == subject)
                .where(GradesFinally.quarter == quarter)
                .values(grade=new_grade)
                .returning(GradesFinally)
            )
            result = await session.execute(statement)
            updated_grade = result.scalars().first()
            if updated_grade:
                await session.commit()
                return updated_grade
            return None

    async def delete_finally_grades_by_user_id(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> None:
        async with self.session_manager(outer_session) as session:
            statement = select(GradesFinally).where(GradesFinally.user_id == user_id)
            result = await session.execute(statement)
            grades = result.scalars().all()
            for grade in grades:
                await session.delete(grade)
            await session.commit()
