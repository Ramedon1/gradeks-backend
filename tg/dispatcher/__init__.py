from aiogram import Dispatcher

from tg.dispatcher.admin import admin_router
from tg.dispatcher.inline import inline_router
from tg.dispatcher.main import main_router

dp = Dispatcher(skip_updates=True)

dp.include_router(main_router)
dp.include_router(admin_router)
dp.include_router(inline_router)