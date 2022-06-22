import os
from typing import Optional, Tuple

from dotenv import load_dotenv

load_dotenv()


# TODO: ПРОВЕРКА КОНФИГА
class Config:
    bot_name: str = os.getenv('BOT_NAME')  # TODO: добавить переменную окружения
    # telegram
    tg_token: str = os.getenv('API_TOKEN')
    webhook_path: str = '/'
    webhook_url: str = os.getenv('WEBHOOK_URL')
    # bot config
    suggest_group_id: str = os.getenv('SUGG_ID')
    recipient_chat_id: str = os.getenv('CHANNEL_ID')
    root_id: int = int(os.getenv('ADMIN_ID'))
    admins: Tuple[int] = (root_id,)
    moderators: Tuple[int] = (root_id,)
    # application
    app_host: str = os.getenv('WEBAPP_HOST')
    app_port: str = os.getenv('WEBAPP_PORT')
    # db
    db_url = os.getenv('DB_URL')  # TODO: сделать переменную DB_URL вместо MONGODB_URL
    cache_url = os.getenv('CACHE_URL')

    # services
    class Instagram:
        login: Optional[str] = os.getenv('INST_LOGIN')
        password: Optional[str] = os.getenv('INST_PASS')


POST_COUNT_IN_WEEK = 25
sugg_post_description = f'Прислали через @{Config.bot_name}'
