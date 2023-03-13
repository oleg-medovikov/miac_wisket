from .dispetcher import dp
from aiogram import types
import pandas as pd
import os

from clas import User, Worker, Work_Group
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
    *Список рабочих групп*
        /get_Work_Groups
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')


async def send_excel(message: types.Message, df: pd.DataFrame, file: str):
    "отправка форматированного файла"
    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    os.remove(file)

Dict_excel = {
    'get_Users':       'temp/Users.xlsx',
    'get_Workers':     'temp/Workers.xlsx',
    'get_Work_Groups': 'temp/Work_Groups.xlsx',
        }


@dp.message_handler(commands=Dict_excel.keys())
async def get_workers_file(message: types.Message):
    "вытаскиваем из базы данные и запихиваем в эксель"
    await delete_message(message)

    USER = await User.get(message['from']['id'])

    if not USER.admin:
        return None
    command = message.text.replace('/', '')

    func = {
        'get_Users':        User.get_all(),
        'get_Workers':      Worker.get_all(),
        'get_Work_Groups':  Work_Group.get_all(),
        }.get(command)

    list_ = await func

    df = pd.DataFrame(data=list_)

    await send_excel(message, df, Dict_excel.get(command))
