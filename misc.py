from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from etc.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
