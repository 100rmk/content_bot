import os
from typing import Optional, Tuple, List

from dotenv import load_dotenv

load_dotenv()


class Config:
    bot_name: str = os.getenv('BOT_NAME')
    watermark_text: str = os.getenv('WATERMARK_TEXT')
    # telegram
    tg_token: str = os.getenv('API_TOKEN')
    webhook_path: str = '/'
    webhook_url: str = os.getenv('WEBHOOK_URL')
    # bot config
    suggest_group_id: str = os.getenv('SUGG_ID')
    recipient_chat_id: str = os.getenv('CHANNEL_ID')
    subscriber_group_id: str = os.getenv('SUB_ID')
    root_id: int = int(os.getenv('ADMIN_ID'))
    admins: List[int] = [root_id, ]
    moderators: List[Optional[int]] = [root_id, ]
    subscribers: List[Optional[int]] = [root_id, ]
    post_count_in_week = os.getenv('POST_COUNT_IN_WEEK', 25)
    # application
    app_host: str = os.getenv('WEBAPP_HOST')
    app_port: str = os.getenv('WEBAPP_PORT')
    # db
    db_url = os.getenv('DB_URL')
    cache_url = os.getenv('CACHE_URL') + bot_name
    tz = int(os.getenv('TZ', 3))
    # logger
    sentry_dsn = os.getenv('SENTRY_DSN')


class Commands:
    default: List[Tuple[str, str]] = []
    subscribers: List[Tuple[str, str]] = []
    moderators: List[Tuple[str, str]] = []
    admins: List[Tuple[str, str]] = []

    @classmethod
    def init_roles(cls):
        cls.subscribers += cls.default
        cls.moderators += cls.subscribers
        cls.admins += cls.moderators

    @classmethod
    def get_commands(cls, role: str):
        return '\n'.join(f'{command}: {description}' for command, description in cls.__dict__[role])


sugg_post_description = f'Прислали через @{Config.bot_name}'
