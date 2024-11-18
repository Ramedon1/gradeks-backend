from aiogram.fsm.state import StatesGroup, State


class AdminLinkDiaryStates(StatesGroup):
    telegram_id = State()
    user_id = State()
    diary_id = State()
