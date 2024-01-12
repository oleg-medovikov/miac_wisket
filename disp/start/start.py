from disp.start import router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    """
    начальная команда бота
    """

    await message.answer("привет!")
