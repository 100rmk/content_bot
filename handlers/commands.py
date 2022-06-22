from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from db.fsm import GroupState
from main import db
from other.text import WELCOME, INFO, NOT_FOUND, UNBANNED, SEND_THE_LINK


async def start(message: types.Message):
    welcome_text = WELCOME
    return SendMessage(chat_id=message.chat.id, text=welcome_text)


async def unban(message: types.Message):
    username = message.get_args()
    resp = db.unban_user(username=username)
    if resp is None:
        return SendMessage(chat_id=message.chat.id, text=f'{username} ' + NOT_FOUND)

    return SendMessage(chat_id=message.chat.id, text=f'{username} ' + UNBANNED)


async def info(message: types.Message):
    welcome_text = INFO
    return SendMessage(chat_id=message.chat.id, text=welcome_text)


async def advertisement(message: types.Message):
    await GroupState.advertising_link.set()
    return SendMessage(chat_id=message.chat.id, text=SEND_THE_LINK)
