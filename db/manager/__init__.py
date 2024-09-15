from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from db.manager.base import DbManagerBase
from db.manager.distribution import DbManagerDistribution
from db.manager.grades import DbManagerGrades
from db.manager.referral import DbManagerReferrals
from db.manager.users import DbManagerUsers
from db.session import engine


class DbManager:
    def __init__(self, db_engine: AsyncEngine):
        self.engine = db_engine
        self.users: DbManagerUsers = DbManagerUsers(db_engine, self)
        self.grades: DbManagerGrades = DbManagerGrades(db_engine, self)
        self.distribution: DbManagerDistribution = DbManagerDistribution(
            db_engine, self
        )
        self.base: DbManagerBase = DbManagerBase(db_engine, self)
        self.referral: DbManagerReferrals = DbManagerReferrals(db_engine, self)

    def session(self) -> AsyncSession:
        return self._async_session()

    def _async_session(self) -> AsyncSession:
        return AsyncSession(self.engine)

    @asynccontextmanager
    async def session_manager(
        self, outer_session: AsyncSession | None = None
    ) -> AsyncIterator[AsyncSession]:
        session = outer_session or self.session()
        if not outer_session:
            await session.__aenter__()
        try:
            yield session
        finally:
            if not outer_session:
                await session.__aexit__(None, None, None)

    async def close(self) -> None:
        await self.engine.dispose()


db_manager: DbManager = DbManager(engine)
