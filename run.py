import asyncio

import uvicorn

from tg.dispatcher import dp
from web.app import fastapi_app


async def start_bot():
    from aiogram.methods import DeleteWebhook

    from tg.bot import bot

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


async def start_scheduler():
    from scheduler.scheduler_grades import main

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


async def start_server():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0")
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    await asyncio.gather(start_bot(), start_server(), start_scheduler())


asyncio.run(main())
