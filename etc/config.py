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

MONGODB_URL = os.getenv('MONGODB_URL')
