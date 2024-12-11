from uuid import UUID

from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.distribution import Distribution
from db.models.users import User
from web.models.users.user import SpecDiaryInfo


class DbManagerUsers(DbManagerBase):

    async def create_user(
        self,
        telegram_id: int,
        first_name: str | None,
        last_name: str | None,
        username: str | None,
        telegram_hash: str,
        outer_session: AsyncSession | None = None,
    ) -> User:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            new_user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                telegram_hash=telegram_hash,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user

    async def get_spec_diary_info(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> SpecDiaryInfo:
        async with self.session_manager(outer_session) as session:
            diary_link = (
                await session.exec(
                    select(User.diary_link).where(User.user_id == user_id)
                )
            ).one()
            diary_id = (
                await session.exec(select(User.diary_id).where(User.user_id == user_id))
            ).one()

            return SpecDiaryInfo(
                diary_link=diary_link,
                diary_id=diary_id,
            )

    async def get_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> User | None:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            statement = select(User).where(User.user_id == user_id)
            result = await session.exec(statement)  # type: ignore
            user = result.one_or_none()

            return user

    async def get_user_by_telegram_id(
        self, telegram_id: int, outer_session: AsyncSession | None = None
    ) -> User | None:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            statement = select(User).where(User.telegram_id == telegram_id)
            result = await session.exec(statement)  # type: ignore
            user = result.one_or_none()
            return user

    async def get_grade_type(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> str:
        async with self.session_manager(outer_session) as session:
            grade_type = (
                await session.exec(
                    select(User.grade_type).where(User.user_id == user_id)
                )
            ).one_or_none()

            return grade_type

    async def change_grade_type(
        self,
        user_id: str | UUID,
        grade_type: str,
        outer_session: AsyncSession | None = None,
    ) -> str:
        async with self.session_manager(outer_session) as session:
            statement = (
                update(User)
                .where(User.user_id == user_id)
                .values(grade_type=grade_type)
            )
            await session.exec(statement)
            await session.commit()

            return grade_type

    async def connect_diary(
        self,
        user_id: str | UUID,
        diary_id: str,
        outer_session: AsyncSession | None = None,
    ):
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            statement = (
                update(User)
                .where(User.user_id == user_id)
                .values(diary_id=diary_id, diary_link=True)
            )
            await session.exec(statement)  # type: ignore
            await session.commit()

    async def get_telegram_id_by_user_id(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> int:
        async with self.session_manager(outer_session) as session:
            telegram_id = (
                await session.exec(
                    select(User.telegram_id).where(User.user_id == user_id)
                )
            ).one_or_none()

            return telegram_id

    async def get_users_diary_connected(
        self, outer_session: AsyncSession | None = None
    ) -> list[User]:
        async with self.session_manager(outer_session) as session:
            statement = select(User).where(User.diary_link == True)
            result = await session.exec(statement)
            users = result.all()

            return users

    async def user_scheduler_grades(
        self, outer_session: AsyncSession | None = None
    ) -> list[User]:
        async with self.session_manager(outer_session) as session:
            statement = (
                select(User)
                .join(Distribution, User.user_id == Distribution.user_id)
                .where(
                    User.diary_link == True,
                    User.is_active == True,
                    Distribution.distribution_status == True,
                )
            )
            result = await session.exec(statement)
            users = result.all()

            return users

    async def get_all_users(
        self, outer_session: AsyncSession | None = None
    ) -> list[User]:
        async with self.session_manager(outer_session) as session:
            statement = select(User)
            result = await session.exec(statement)
            users = result.all()

            return users

    async def get_user_id_by_telegram_id(
        self, telegram_id: int, outer_session: AsyncSession | None = None
    ) -> str | UUID:
        async with self.session_manager(outer_session) as session:
            user_id = (
                await session.exec(
                    select(User.user_id).where(User.telegram_id == telegram_id)
                )
            ).one_or_none()

            return user_id
