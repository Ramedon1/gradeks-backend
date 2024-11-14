import os
import re
import shutil

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import FSInputFile, Message

from tg.bot import bot
from tg.common.play_now_keyboard import get_play_now_keyboard

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message, command: CommandObject):
    keyboard = get_play_now_keyboard()
    profile_img = await bot.get_user_profile_photos(
        user_id=message.from_user.id, limit=1
    )

    if profile_img.photos:
        file_id = profile_img.photos[0][0].file_id
        file_info = await bot.get_file(file_id)

        avatars_dir = "avatars"
        if not os.path.exists(avatars_dir):
            os.makedirs(avatars_dir)

        file_path = f"{avatars_dir}/{message.from_user.id}_avatar.jpg"

        downloaded_file = await bot.download_file(file_info.file_path)
        with open(file_path, "wb") as f:
            f.write(downloaded_file.read())

    else:
        shutil.copy(
            "avatars/default_avatar.png", f"avatars/{message.from_user.id}_avatar.jpg"
        )

    if command.args:
        if re.match(r"r_[0-9]+", command.args):
            keyboard = get_play_now_keyboard(ref=command.args.replace("r_", ""))

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
