from disp.start import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot

from func import add_keyboard, update_message

from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "settings"))
async def settings(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут несколько кнопок для добавления групп, воркеров и прочего
    """
    DICT = {}

    callback_data.action = "create_group"
    DICT["создать группу"] = callback_data.pack()

    callback_data.action = "start"
    DICT["назад"] = callback_data.pack()

    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            "Доступные настройки бота:",
            add_keyboard(DICT),
            image_name="settings",
        )
