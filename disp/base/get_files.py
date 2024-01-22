from disp.base import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot

from func import (
    add_keyboard,
    update_message,
    get_all_Struct,
    get_all_Worker,
    get_svup_worker,
)
from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "get_files"))
async def get_files(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут возвращаем файлии для редактирования базы
    """
    func = {
        1: get_all_Struct(),
        2: get_all_Worker(),
        3: get_svup_worker(),
    }[callback_data.file]

    file = await func

    DICT = {}
    callback_data.action = "settings"
    callback_data.file = 0
    DICT["назад"] = callback_data.pack()

    if file == "":
        file = None
        mess = "не смог сформировать файл"
    else:
        mess = "Заполните файл и киньте мне его обратно в чат. Я применю изменения"
    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            mess,
            add_keyboard(DICT),
            # image_id=4
            image_name="files",
            file_path=file,
        )
