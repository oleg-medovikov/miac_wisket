import asyncio
import aioschedule
import logging

from func import get_time_start, get_time_stop


async def scheduler():
    aioschedule.every(1).hours.do(get_time_start, date=None)
    aioschedule.every(1).hours.do(get_time_stop, date=None)
    # aioschedule.every(1).hours.do(get_time_stop)
    # aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def test_send():
    logging.info("Тестовое срабатывание планировщика")
