from disp.start import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot

from func import add_keyboard, update_message

from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "settings"))
async def settings(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут несколько кнопок для добавления групп, воркеров и прочего
    1 - редактируем группы
    2 - редактируем воркеров
    """
    DICT = {}

    callback_data.action = "get_files"
    callback_data.file = 1
    DICT["ред. группы"] = callback_data.pack()

    callback_data.file = 2
    DICT["ред. работников"] = callback_data.pack()

    callback_data.action = "start"
    callback_data.file = 0
    DICT["назад"] = callback_data.pack()

    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            "Доступные настройки бота:",
            add_keyboard(DICT),
            image_name="settings",
        )
