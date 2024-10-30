import asyncio

from aiogram.methods import DeleteWebhook

from tg.bot import bot
from tg.dispatcher import dp


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


asyncio.run(main())
