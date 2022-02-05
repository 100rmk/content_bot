import logging

import pymongo
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from instaloader import Instaloader

from etc.config import API_TOKEN, MONGODB_URL, INST_META

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_mongo = pymongo.MongoClient(MONGODB_URL)

inst_loader = Instaloader(user_agent=INST_META['user_agent'])
inst_loader.login(INST_META['login'], INST_META['password'])
