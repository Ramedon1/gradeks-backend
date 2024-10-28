import uuid
from contextlib import asynccontextmanager
from functools import wraps
from typing import TYPE_CHECKING, AsyncIterator, TypeVar

from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from common import context_logger
from common.context_logger import Context, SpanId

if TYPE_CHECKING:
    from db.manager import DbManager

logger = context_logger.get(__name__)
T = TypeVar("T")


class DbManagerBase:
    def __init__(self, engine: AsyncEngine, root_manager: "DbManager" = None):
        self.engine: AsyncEngine = engine
        self.root_manager: DbManager | None = root_manager

        for attr_name, attr_value in self.__class__.__dict__.items():
            if attr_name.startswith("_") or isinstance(attr_value, property):
                continue
            if (
                not attr_name.startswith("_")
                and hasattr(attr_value, "__annotations__")
                and "return" in attr_value.__annotations__
            ):
                setattr(self, attr_name, self.decorate_context(attr_value))

    def decorate_context(self, func: T) -> T:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            span_id_token = SpanId.set(str(uuid.uuid4()))
            context_token = Context.set({"func_args": args, "func_kwargs": kwargs})
            logger.debug(f"(DB.{func.__name__}) Call method with {args=} {kwargs=}")
            try:
                try:
                    result = await func(self, *args, **kwargs)
                except InterfaceError as e:
                    logger.exception(
                        f"(DB.{func.__name__}) Connection to db is loosed, try to reconnect"
                    )
                    result = await func(self, *args, **kwargs)
            except Exception as e:
                logger.exception(f"(DB.{func.__name__}) Error during execution")
                raise
            else:
                logger.debug(f"(DB.{func.__name__}) Method executed with {result=}")
                return result
            finally:
                SpanId.reset(span_id_token)
                Context.reset(context_token)

        return wrapper

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
