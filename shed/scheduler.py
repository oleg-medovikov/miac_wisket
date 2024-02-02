import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from func import get_time_start, get_time_stop

# Инициализация планировщика
scheduler = AsyncIOScheduler()


async def start_scheduler():
    scheduler.add_job(get_time_start, "cron", hour="*", minute=21)
    scheduler.add_job(get_time_stop, "cron", hour="*", minute=0)
    # scheduler.add_job(test_send, "interval", seconds=5)
    scheduler.start()


async def test_send():
    logging.info("Тестовое срабатывание планировщика")
