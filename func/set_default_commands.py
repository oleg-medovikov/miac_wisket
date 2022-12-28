from aiogram.types import BotCommand


async def set_default_commands(dp):
    commands = [
        BotCommand(
            command="start",
            description="Приветсвие"
            ),
        BotCommand(
            command="files",
            description="Файлы для редактирования базы"
            ),
        BotCommand(
            command="journal",
            description="Команды ведения общего журнала"
            ),


        ]

#    await dp.bot.delete_my_commands(commands)
    await dp.bot.set_my_commands(commands)
