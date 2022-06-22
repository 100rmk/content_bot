import logging

import aiocron
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from db.mongodb import MongoDB
from db.redis import AsyncRedisCache
from etc.config import Config
from etc.filters import AdminFilter, NicknameFilter, ModerFilter
from handlers.registrator import register_handlers
from service.instagram import Instagram
from service.schedule_tasks import update_users_sugg_count, upload_cache_db

bot = Bot(token=Config.tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
db = MongoDB(mongo_url=Config.db_url, bot_name=Config.bot_name)
cache = AsyncRedisCache(url=Config.cache_url)
instagram = Instagram(username=Config.Instagram.login, password=Config.Instagram.password).login()
any(dp.filters_factory.bind(filter_) for filter_ in (AdminFilter, NicknameFilter, ModerFilter))


async def on_startup(dp):
    await bot.set_webhook(Config.webhook_url)
    aiocron.crontab('0 0 * * FRI', update_users_sugg_count, args=(db, ))  # every 00:00 on Friday
    aiocron.crontab('*/20 * * * *', upload_cache_db, args=(db, cache))  # every 20 minutes


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    register_handlers(dispatcher=dp)
    start_webhook(
        dispatcher=dp,
        webhook_path=Config.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=Config.app_host,
        port=Config.app_port,
    )
