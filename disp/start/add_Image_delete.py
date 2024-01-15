from disp.start import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot

from func import add_keyboard, update_message

from mdls import Image
from conf import CallAny


@router.callback_query(CallAny.filter(F.action == "image_delete"))
async def add_Image_delete(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    вместо добавления названия картинке, удаляем ее из базы
    """

    await Image.delete.where(Image.id == callback_data.image_id).gino.status()

    callback_data.action = "start"
    DICT = {"хорошо": callback_data.pack()}

    if isinstance(callback.message, Message):
        await update_message(
            bot,
            callback.message,
            "Картинка удалена из базы",
            add_keyboard(DICT),
            image_id=callback_data.image_id,
        )
