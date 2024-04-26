from disp.admin import router
from aiogram.types import Message
import pandas as pd
import logging


# Обработчик для сообщений, являющихся ответами
@router.message()
async def reply_handler(message: Message):
    # Получаем сообщение, на которое ответили
    replied_message = message.reply_to_message
    # Отправляем ответ
    await message.answer(f"Вы ответили на сообщение: {replied_message.text}")
