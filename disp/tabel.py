from .dispetcher import dp
from aiogram import types

from clas import Work_Group
from func import delete_message, write_styling_excel_file


@dp.message_handler(commands='tabel')
async def get_tabel_file(message: types.Message):
    await delete_message(message)

    WORKERS = await Work_Group.get_workers(message['from']['id'])

    await message.answer(str(WORKERS), parse_mode='html')
