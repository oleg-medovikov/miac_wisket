from aiogram.types import BotCommand

DICT = {
    'start': 'Приветсвие',
    'files': 'Файлы для редактирования базы',
    'journal': 'Команды ведения общего журнала',
    'tabel': 'Получить табель посещаемости (месяц)',
    }


async def set_default_commands(dp):
    commands = []

    for key, value in DICT.items():
        commands.append(BotCommand(
            command=key,
            description=value
            ))

#    await dp.bot.delete_my_commands(commands)
    await dp.bot.set_my_commands(commands)
