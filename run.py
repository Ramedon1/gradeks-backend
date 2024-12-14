import asyncio

import uvicorn

import settings
from common.common import log_task_exception
from tg.bot import bot
from tg.dispatcher import dp
from web.app import fastapi_app

admin_id = int(settings.ADMIN_ID)


async def start_bot():
    from aiogram.methods import DeleteWebhook

    from tg.bot import bot

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


async def start_scheduler():
    from scheduler.scheduler_grades import main

    await main()


async def start_server():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0")
    server = uvicorn.Server(config)
    await server.serve()


async def start_tasks():
    tasks = [
        asyncio.create_task(start_bot(), name="bot"),
    ]

    for task in tasks:
        task.add_done_callback(lambda t: asyncio.create_task(log_task_exception(t)))

    await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    await start_tasks()


if __name__ == "__main__":
    asyncio.run(main())
