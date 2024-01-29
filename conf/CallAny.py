from aiogram.filters.callback_data import CallbackData


class CallAny(CallbackData, prefix="any"):
    action: str
    user_id: int = 0
    image_id: int = 0
    file: int = 0
    year: int = 0
    month: int = 0
    k: int = 0
