import logging


async def get_chat_ids(message, bot):
    # Получаем ID чата из сообщения
    chat_id = message.chat.id
    # Отправляем запрос к Telegram Bot API
    chat = await bot.get_chat(chat_id)
    logging.info(str(chat))
    # Получаем JSON ответ
    # Отправляем информацию о чате пользователю
    await message.answer(f"Информация о чате:\n{chat}")
