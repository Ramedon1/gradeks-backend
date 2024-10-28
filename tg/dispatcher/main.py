import re

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart, Filter
from aiogram.types import Message

import settings
from tg.common.play_now_keyboard import get_play_now_keyboard

main_router = Router()


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text


@main_router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    keyboard = get_play_now_keyboard()
    if command.args:
        if re.match(r"r_[0-9]+", command.args):
            keyboard = get_play_now_keyboard(ref=command.args.replace("r_", ""))

    await message.answer(
        text=(f"TAP TAP TAP\n" f"\n" f"Subscribe channel — t.me/ramedon"),
        reply_markup=keyboard,
    )
