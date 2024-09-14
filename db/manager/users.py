from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.users import User


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
                is_active=True,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user

    async def get_diary_link(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> bool:
        async with self.session_manager(outer_session) as session:
            statement = select(User.diary_link).where(User.user_id == user_id)
            result = await session.exec(statement)
            user = result.one_or_none()

            return user

    async def get_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> User | None:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            statement = select(User).where(User.user_id == user_id)
            result = await session.exec(statement)  # type: ignore
            user = result.one_or_none()

            return user
