from datetime import datetime
from uuid import UUID

from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.models.distribution import Distribution


class DbManagerDistribution(DbManagerBase):
    async def create_distributions_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> Distribution | None:
        async with self.session_manager(outer_session) as session:
            new_distribution = Distribution(
                user_id=user_id,
                distribution_status=True,
            )
            session.add(new_distribution)

            await session.commit()
            await session.refresh(new_distribution)

            return new_distribution

    async def get_distribution_status_user(
        self, user_id: str | UUID, outer_session: AsyncSession | None = None
    ) -> bool | None:
        async with self.session_manager(outer_session) as session:
            statement = select(Distribution.distribution_status).where(
                Distribution.user_id == user_id
            )
            result = await session.exec(statement)
            distribution = result.one_or_none()

            return distribution

    async def get_distribution_users_active(
        self,
        user_id: str | UUID,
        distribution_type: str,
        limit: int = 25,
        offset: int = 0,
        outer_session: AsyncSession | None = None,
    ) -> list[Distribution]:
        async with self.session_manager(outer_session) as session:
            statement = (
                (
                    select(Distribution)
                    .where(Distribution.user_id == user_id)
                    .where(Distribution.distribution_type == distribution_type)
                    .where(Distribution.distribution_status == True)
                )
                .offset(offset)
                .limit(limit)
            )
            result = await session.exec(statement)
            distribution: list[Distribution] = list(result.all())

            return distribution

    async def activate_distribution(
        self,
        user_id: str | UUID,
        outer_session: AsyncSession | None = None,
    ) -> None:
        async with self.session_manager(outer_session) as session:  # type: AsyncSession   # fmt: skip
            statement = (
                update(Distribution)
                .where(Distribution.user_id == user_id)
                .values(distribution_status=True)
            )
            await session.exec(statement)  # type: ignore
            await session.commit()

    async def deactivate_distribution(
        self,
        user_id: str | UUID,
        outer_session: AsyncSession | None = None,
    ) -> None:
        async with self.session_manager(outer_session) as session:
            statement = (
                update(Distribution)
                .where(Distribution.user_id == user_id)
                .values(distribution_status=False)
            )
            await session.exec(statement)
            await session.commit()
