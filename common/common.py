import asyncio
from datetime import UTC, datetime

from sqlmodel import Field

import settings
from tg.bot import bot


def pg_now() -> datetime:
    return datetime.now().astimezone(UTC).replace(tzinfo=None)


def CreatedAtField(index=False):  # noqa
    return Field(
        default_factory=pg_now,
        nullable=False,
        index=index,
    )


async def log_task_exception(task: asyncio.Task):
    if task.exception():
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Task {task.get_name()} failed with exception: {task.exception()}",
        )
