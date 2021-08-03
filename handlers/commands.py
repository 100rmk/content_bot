from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from db import db
from misc import dp


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    welcome_text = '''Шалом!
Бот принимает только фото или видео(до 20мб.), комментарии(описание под контентом) не учитываются.
Правила предложки:
1. Не больше 25 мемов в неделю.
2. Обязательно иметь username в телеграме (Настройки->Изменить->Имя пользователя).
3. На мемасах не должно быть водных знаков.
    '''
    return SendMessage(message.chat.id, welcome_text)


@dp.message_handler(is_admin=True, commands=["unban"])
async def start_command(message: types.Message):
    username = message.get_args()
    resp = db.unban_user(username)
    if resp is None:
        return SendMessage(message.chat.id, f'{username} не найден, бан не снят')

    return SendMessage(message.chat.id, f'{username} разбанен')


@dp.message_handler(is_admin=True, commands=["month"])
async def start_command(message: types.Message):
    month = int(message.get_args())
    result = db.top_10_month(month)
    return SendMessage(message.chat.id, result)


@dp.message_handler(commands=["info"])
async def start_command(message: types.Message):
    welcome_text = '''
Бот принимает только фото или видео(до 20мб.), комментарии(описание под контентом) не учитываетются.

Деньги за мемы:
    В конце каждого месяца, на основе лайков, определяется топ 3 мема из предложки. Авторы лучших мемов получают денежное вознаграждение. 
    Фонд месяца объявляется в группе t.me/vidmem
Один автор не может занять несколько призовых. В спорных моментах учитываются дизлайки.

За что можно получить бан:
За спам в предложку и ненадлежащий контент, т.е. дикпики слать не нужно.

И еще немного правил:
1. Не больше 25 мемов в неделю.
2. Обязательно иметь username в телеграме (Настройки->Изменить->Имя пользователя).
3. На мемасах не должно быть водных знаков.
    '''
    return SendMessage(message.chat.id, welcome_text)
