from aiogram import Bot, Dispatcher

from conf import TELEGRAM_API

import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
logging.getLogger('schedule').addHandler(logging.NullHandler())


bot = Bot(token=TELEGRAM_API)
dp = Dispatcher(bot)
