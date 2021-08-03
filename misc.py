import logging

import pymongo
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from etc.config import API_TOKEN, MONGODB_URL

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db_mongo = pymongo.MongoClient(MONGODB_URL)
