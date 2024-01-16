from disp.start import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot

from func import add_keyboard, update_message, get_all_Struct
from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "get_files"))
async def get_files(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут возвращаем файлии для редактирования базы
    """
    func = {
        # 1: get_all_Worker(),
        1: get_all_Struct(),
    }[callback_data.file]

    file = await func

    DICT = {}
    callback_data.action = "settings"
    callback_data.file = 0
    DICT["назад"] = callback_data.pack()

    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            "Заполните файл и киньте мне его обратно в чат. Я применю изменения",
            add_keyboard(DICT),
            # image_id=4
            image_name="files",
            file_path=file,
        )
