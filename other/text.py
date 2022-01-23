# inline_names
AD_GOTO = 'Перейти'
INLINE_TEXT = {
    'success': 'залетел',
    'fail': 'улетел',
    'thumbUp': '👍',
    'thumbDown': '👎'
}
# commands.py
WELCOME = '''Шалом!
Бот принимает только фото или видео(до 20мб.), комментарии(описание под контентом) не учитываются.
Правила предложки:
1. Не больше 25 мемов в неделю.
2. Обязательно иметь username в телеграме (Настройки->Изменить->Имя пользователя).
3. На мемасах не должно быть водных знаков.
    '''
INFO = '''
Бот принимает только фото или видео(до 20мб.), комментарии(описание под контентом) не учитываетются.

За что можно получить бан:
За спам в предложку и ненадлежащий контент, т.е. дикпики слать не нужно.

И еще немного правил:
1. Не больше 25 мемов в неделю.
2. Обязательно иметь username в телеграме (Настройки->Изменить->Имя пользователя).
3. На мемасах не должно быть водных знаков.
    '''
NOT_FOUND = 'не найден'
UNBANNED = 'разбанен'
SEND_THE_LINK = 'Отправьте ссылку на рекламу'

# content.py
MODERATOR_NAME = '@wtfout'
MESSAGE_FOR_BANNED_USER = f'''Извините, но вы в бане, видимо вы запостили контент противоречащий нашим нормам морали. 
                           Если это не так и вы попали в бан ошибочно, напишите {MODERATOR_NAME}'''
LIMIT_EXCEEDED = 'Лимит мемов исчерпан. Счетчик обновится в пятницу'
POST_ACCEPTED = 'Мем принят, на этой неделе вы можете скинуть мемов:'
SEND_AD_POST = 'Отправьте рекламный пост'
AD_POST_SENT = 'Рекламный пост отправлен'
PROCESSING = 'Идет обработка...'

# callback.py
LIKES_TIMEOUT = 'Время для лайков истекло'
USER_BANNED = 'Забанен пользователь: '
DELETE_FAIL = 'Нельзя удалить, удалите руками'
DELETED = 'Удалено'
POST_SOON = 'Мем скоро будет запощен'
POST_FAIL = 'Мем нихуя не запощен'