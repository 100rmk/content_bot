from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from etc.config import API_TOKEN, MONGODB_URL
import logging
import pymongo

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = pymongo.MongoClient(MONGODB_URL)
db_posts = db.tg_memvid.posts
