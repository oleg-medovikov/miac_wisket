from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CallAny(CallbackData, prefix="any"):
    action: str
    user_id: int = 0
    image_id: int = 0
