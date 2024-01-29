import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from conf import settings, db
from func import set_default_commands
from disp import start, base, admin
from shed import scheduler


logging.basicConfig(level=logging.INFO)
# logging.getLogger("schedule").propagate = False
# logging.getLogger("schedule").addHandler(logging.NullHandler())
# logging.getLogger("gino.engine._SAEngine").setLevel(logging.ERROR)


async def on_startup():
    bot = Bot(token=settings.BOT_API)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(start.router, base.router, admin.router)

    await db.set_bind(settings.PSQL)
    await db.gino.create_all()
    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot), scheduler())


async def on_shutdown():
    await db.pop_bind().close()


if __name__ == "__main__":
    try:
        asyncio.run(on_startup())
    except KeyboardInterrupt:
        asyncio.run(on_shutdown())
