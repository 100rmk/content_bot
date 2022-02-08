import logging

import pymongo
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from instaloader import Instaloader
from filters import AdminFilter, NicknameFilter, ModerFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from etc.config import API_TOKEN, MONGODB_URL, INST_META
from other import text

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_mongo = pymongo.MongoClient(MONGODB_URL)

# reaction buttons
inline_reaction = InlineKeyboardMarkup(row_width=2)
like_btn = InlineKeyboardButton(text.INLINE_TEXT['thumbUp'], callback_data='up')
dislike_btn = InlineKeyboardButton(text.INLINE_TEXT['thumbDown'], callback_data='down')
inline_reaction.add(like_btn, dislike_btn)

# moder buttons
inline_moderation = InlineKeyboardMarkup(row_width=2)
post_btn = InlineKeyboardButton('POST', callback_data='post')
remove_btn = InlineKeyboardButton('REMOVE', callback_data='remove')
ban_btn = InlineKeyboardButton('BAN', callback_data='ban')
inline_moderation.add(post_btn).add(remove_btn, ban_btn)

# filters
dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(NicknameFilter)
dp.filters_factory.bind(ModerFilter)

# inst login buttons
inst_loader = Instaloader(user_agent=INST_META['user_agent'])
inst_loader.login(INST_META['login'], INST_META['password'])
