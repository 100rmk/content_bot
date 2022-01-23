import logging

import pymongo
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from etc.config import API_TOKEN, MONGODB_URL

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_mongo = pymongo.MongoClient(MONGODB_URL)
