from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncIterator, TypeVar

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

if TYPE_CHECKING:
    from db.manager import DbManager


class DbManagerBase:
    def __init__(self, engine: AsyncEngine, root_manager: "DbManager" = None):
        self.engine: AsyncEngine = engine
        self.root_manager: DbManager | None = root_manager

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
