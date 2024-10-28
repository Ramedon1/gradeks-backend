from aiogram import Dispatcher

from tg.dispatcher.main import main_router

dp = Dispatcher()
dp.include_router(main_router)
