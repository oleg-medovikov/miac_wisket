from .dispetcher import dp
from aiogram import types

from clas import User
from func import delete_message


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None

    MESS = f'добрый день, {USER.name}!'
    await message.answer(MESS, parse_mode='html')
