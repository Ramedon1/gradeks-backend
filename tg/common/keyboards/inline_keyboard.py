from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_send():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖",
                    url="https://t.me/gradeksbot",
                ),
            ],
        ]
    )
    return keyboard
