import asyncio

from tg.bot import bot
from tg.dispatcher import dp


async def main() -> None:
    await dp.start_polling(bot, skip_updates=True)


asyncio.run(main())
