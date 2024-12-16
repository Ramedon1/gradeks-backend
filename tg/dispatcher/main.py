import re

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import FSInputFile, Message

from tg.bot import bot
from tg.common.keyboards.play_now_keyboard import get_play_now_keyboard

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    keyboard = get_play_now_keyboard()

    animation = FSInputFile("static/gradeks.mp4", filename="gradeks.mp4")

    await bot.send_animation(
        animation=animation,
        chat_id=message.from_user.id,
        caption=(
            "Привет, друг! Это Gradeks 👋\n\n"
            "Подключай электронный дневник и следи за оценками.\n\n"
            "Внизу есть небольшая инструкция. Вероятно, это всё, что надо знать."
        ),
        reply_markup=keyboard,
    )
