GRADE_CHECKING_ENABLED = True


async def toggle_grade_checking() -> bool:
    """
    Переключает состояние проверки оценок.
    Возвращает новое состояние.
    """
    global GRADE_CHECKING_ENABLED
    GRADE_CHECKING_ENABLED = not GRADE_CHECKING_ENABLED
    return GRADE_CHECKING_ENABLED


async def is_grade_checking_enabled() -> bool:
    """
    Возвращает состояние проверки оценок.
    """
    return GRADE_CHECKING_ENABLED
