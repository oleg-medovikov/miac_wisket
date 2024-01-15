from disp.start import router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F, Bot

from conf import CallAny
from func import update_message, add_keyboard
from mdls import Image


class NewImage(StatesGroup):
    image_id = State()
    name = State()


@router.callback_query(CallAny.filter(F.action == "ask_name_Image"))
async def ask_Image_name(
    callback: CallbackQuery, callback_data: CallAny, state: FSMContext, bot: Bot
):
    await state.update_data(image_id=callback_data.image_id)

    callback_data.action = "add_image_delete"
    DICT = {"удалить картинку": callback_data.pack()}

    await update_message(
        bot,
        callback.message,
        "Напишите название картинки:",
        add_keyboard(DICT),
        image_id=callback_data.image_id,
    )

    # Устанавливаем пользователю состояние "пишет название"
    return await state.set_state(NewImage.name)


@router.message(NewImage.name)
async def update_Image(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    image = await Image.get(user_data["image_id"])

    await image.update(name=user_data["name"]).apply()

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
    DICT = {"Хорошо": CallAny(action="start")}
    await update_message(
        bot,
        message,
        f"Картинка сохранена\nid: {image.id}",
        add_keyboard(DICT),
        image_id=image.id,
    )
