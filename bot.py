import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from etc.config import *
from misc import dp, bot

from schedule_background import run_continuously

import handlers

logging.basicConfig(level=logging.INFO)
stop_run_continuously = None


async def on_startup(dp):
    global stop_run_continuously
    await bot.set_webhook(WEBHOOK_URL)
    stop_run_continuously = run_continuously(interval=60)


async def on_shutdown(dp):
    global stop_run_continuously
    logging.warning('Shutting down..')
    stop_run_continuously.set()
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
