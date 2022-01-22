import os

API_TOKEN = os.getenv('API_TOKEN')

# Settings for webhook
WEBHOOK_PATH = '/'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

POST_COUNT_IN_WEEK = 25
sugg_post_description = 'Прислали через @VidMem_bot'

id_predlojki = 1
my_group = 1337
RECIPIENT_CHAT_ID = my_group
ADMINS = (1337,)  # tuple of admins id

MONGODB_URL = os.getenv('MONGODB_URL')
