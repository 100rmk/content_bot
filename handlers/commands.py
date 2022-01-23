from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from db import db
from db.fsm import GroupState
from misc import dp
from other.text import WELCOME, INFO, NOT_FOUND, UNBANNED, SEND_THE_LINK


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    welcome_text = WELCOME
    return SendMessage(message.chat.id, welcome_text)


@dp.message_handler(is_admin=True, commands=["unban"])
async def unban(message: types.Message):
    username = message.get_args()
    resp = db.unban_user(username)
    if resp is None:
        return SendMessage(message.chat.id, f'{username} ' + NOT_FOUND)

    return SendMessage(message.chat.id, f'{username} ' + UNBANNED)


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    welcome_text = INFO
    return SendMessage(message.chat.id, welcome_text)


@dp.message_handler(is_admin=True, commands=["ad"])
async def advertisment(message: types.Message):
    await GroupState.advertising_link.set()
    return SendMessage(message.chat.id, SEND_THE_LINK)
