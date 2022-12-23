from aiogram.types import BotCommand


async def set_default_commands(dp):
    commands = [
        BotCommand(
            command="start",
            description="Приветсвие"
            ),
        ]

#    await dp.bot.delete_my_commands(commands)
    await dp.bot.set_my_commands(commands)
