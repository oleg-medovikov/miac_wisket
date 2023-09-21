from .dispetcher import dp
from aiogram import types

from clas import User
from func import delete_message, \
    get_time_start, get_time_stop, \
    get_time_start_mounth, get_time_stop_mounth


@dp.message_handler(commands='journal')
async def get_journal_commands(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    MESS = """*Доступные команды для ведения журнала:*

    *Записать время прихода*
        /journal_time_start
    *Записать время прихода за месяц*
        /journal_time_start_mounth
    *записать время ухода*
        /journal_time_stop
    *записать время ухода за месяц*
        /journal_time_stop_mounth
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')


@dp.message_handler(commands=['journal_time_start_mounth'])
async def journal_time_start_mounth_manual(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    await get_time_start_mounth()

    return await message.answer('Done', parse_mode='Markdown')


@dp.message_handler(commands=['journal_time_start'])
async def journal_time_start_manual(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    await get_time_start(False)

    return await message.answer('Done', parse_mode='Markdown')


@dp.message_handler(commands=['journal_time_stop'])
async def journal_time_stop_manual(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None:
        return None
    if not USER.admin:
        return await message.answer(
            "функция для админов",
            parse_mode='Markdown'
            )

    await get_time_stop(scheduler=False)

    return await message.answer('Done', parse_mode='Markdown')
