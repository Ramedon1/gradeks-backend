import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
import sys

sys.path = ['', '..'] + sys.path[1:]

from db import models
from sqlmodel import SQLModel

config = context.config
fileConfig(config.config_file_name)

import settings

config.set_main_option("sqlalchemy.url", settings.POSTGRES_URL)
target_metadata = SQLModel.metadata



def run_migrations_offline() -> None:
    """Offline mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async() -> None:
    """Async 'online' mode"""
    # read the DB URL that we put in config
    url = config.get_main_option("sqlalchemy.url", settings.POSTGRES_URL)
    engine = create_async_engine(url, poolclass=pool.NullPool)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def do_run_migrations(connection):
    """What to run in a synchronous context"""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Wrapper that calls the async function via asyncio.run()"""
    asyncio.run(run_migrations_online_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
