import asyncio
import aioschedule

from clas import User
from func import bot_send_text, get_time_start, get_time_stop


async def scheduler():
    aioschedule.every(1).hours.do(get_time_start, scheduler=True)
    aioschedule.every(1).hours.do(get_time_stop, scheduler=True)
#    aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def test_send():
    USER = await User.get('200712816')

    bot_send_text('Привет от шедулера!', int(USER.u_id))
