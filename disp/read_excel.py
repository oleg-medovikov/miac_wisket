from .dispetcher import dp, bot
from aiogram import types
import pandas as pd
import os

from clas import User, Worker
from func import delete_message

NAMES = {
    'Users.xlsx': ['u_id', 'w_id', 'name', 'name_tg', 'admin'],
    'Workers.xlsx': [
        'w_id', 'id_svup', 'name', 'first_name',
        'mid_name', 'birthday', 'phone', 'date_update'
        ],
    }


@dp.message_handler(content_types='document')
async def read_excel_file(message: types.Message):
    """Работа с файлами которые посылает пользователь"""
    delete_message(message)
    FILE = message['document']
    USER = await User.get(message['from']['id'])

    if USER is None:
        return None

    if not USER.admin:
        return await message.answer('функция для админов')

    if FILE['file_name'] not in NAMES.keys():
        return await message.answer('У файла неправильное имя')

    DESTINATION = 'temp/' + FILE.file_unique_id + 'xlsx'
    await bot.download_file_by_id(
        file_id=FILE.file_id,
        destination=DESTINATION
            )

    try:
        df = pd.read_excel(
            DESTINATION,
            usecols=NAMES.get(FILE['file_name'])
                )
    except Exception as e:
        return await message.answer(str(e))

    df.dropna(inplace=True)
    list_ = df.to_dict('records')

    if FILE['file_name'] == 'Users.xlsx':
        MESS = await User.update(list_)
        await message.answer(MESS)
    elif FILE['file_name'] == 'Workers.xlsx':
        MESS = await Worker.update(list_)
        await message.answer(MESS)

    os.remove(DESTINATION)
