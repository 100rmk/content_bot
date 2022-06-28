from aiogram import types
from aiogram.dispatcher.webhook import SendMessage
from etc.config import Commands, Config
from db.fsm import GroupState
from main import db
from other.text import WELCOME, INFO, NOT_FOUND, UNBANNED, SEND_THE_LINK, EMPTY


async def start(message: types.Message):
    """Стартовая команда, выводит базовую информацию"""
    welcome_text = WELCOME
    return SendMessage(chat_id=message.chat.id, text=welcome_text)


async def unban(message: types.Message):
    """Разбанить пользователя: tg_nickname"""
    username = message.get_args()
    if not username:
        return SendMessage(chat_id=message.chat.id, text=EMPTY)
    resp = db.unban_user(username=username)
    if resp is None:
        return SendMessage(chat_id=message.chat.id, text=f'{username} ' + NOT_FOUND)

    return SendMessage(chat_id=message.chat.id, text=f'{username} ' + UNBANNED)


async def info(message: types.Message):
    """Основная информация"""
    return SendMessage(chat_id=message.chat.id, text=INFO)


async def help_(message: types.Message):
    """Список доступных команд"""
    if message.from_user.id in Config.admins:
        return SendMessage(chat_id=message.chat.id, text=Commands.get_commands(role='admins'))
    elif message.from_user.id in Config.moderators:
        return SendMessage(chat_id=message.chat.id, text=Commands.get_commands(role='moderators'))
    elif message.from_user.id in Config.subscribers:
        return SendMessage(chat_id=message.chat.id, text=Commands.get_commands(role='subscribers'))
    else:
        return SendMessage(chat_id=message.chat.id, text=Commands.get_commands(role='default'))


async def advertisement(message: types.Message):
    """Пост рекламы с кнопкой"""
    await GroupState.advertising_link.set()
    return SendMessage(chat_id=message.chat.id, text=SEND_THE_LINK)
