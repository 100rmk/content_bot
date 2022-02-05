import os

API_TOKEN = os.getenv('API_TOKEN')

# Settings for webhook
WEBHOOK_PATH = '/'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

POST_COUNT_IN_WEEK = 25
sugg_post_description = 'Прислали через @VidMem_bot'

SUGGEST_ID = os.getenv('SUGG_ID')
RECIPIENT_CHAT_ID = os.getenv('CHANNEL_ID')
ADMINS = (int(os.getenv('ADMIN_ID')),)  # tuple of admins id
MODERS = (os.getenv('MODERS_ID'),) + ADMINS  # TODO: get/set from db

MONGODB_URL = os.getenv('MONGODB_URL')

INST_META = {
    'login': os.getenv('INST_LOGIN'),
    'password': os.getenv('INST_PASS'),
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.99 Safari/537.36 '  # TODO: change
}
