from aiogram.fsm.state import State, StatesGroup


class AdminLinkDiaryStates(StatesGroup):
    telegram_id = State()
    user_id = State()
    diary_id = State()
