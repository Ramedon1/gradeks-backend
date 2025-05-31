import asyncio
import logging
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


import re


async def log_task_exception(task: asyncio.Task):
    if task.exception():
        logging.error(task.exception())
        exception_message = str(task.exception())

        sanitized_message = re.sub(r"<.*?>", "", exception_message)
        sanitized_message = sanitized_message.replace("\n", " ")

        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Task {task.get_name()} failed with exception: {sanitized_message}",
        )
