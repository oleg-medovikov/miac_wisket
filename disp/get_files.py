from .dispetcher import dp
from aiogram import types
import pandas as pd
import os

from clas import User, Worker
from func import delete_message, write_styling_excel_file


@dp.message_handler(commands='files')
async def get_files_help(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])

    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    MESS = """*Доступные команды для редактирования базы:*

    *Список юзеров*
        /get_Users
    *Список сотрудников*
        /get_Workers
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')


async def send_excel(message: types.Message, df: pd.DataFrame, file: str):

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    os.remove(file)

Dict_excel = {
    'get_Users':   'temp/Users.xlsx',
    'get_Workers': 'temp/Workers.xlsx',

        }


@dp.message_handler(commands=Dict_excel.keys())
async def get_workers_file(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])

    if not USER.admin:
        return None
    command = message.text.replace('/', '')

    list_ = {
        command == 'get_Users': await User.get_all(),
        command == 'get_Workers': await Worker.get_all(),
        }[True]

    df = pd.DataFrame(data=list_)

    await send_excel(message, df, Dict_excel.get(command))
