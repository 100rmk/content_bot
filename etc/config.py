import os

API_TOKEN = os.getenv('API_TOKEN')

# Settings for webhook
WEBHOOK_PATH = '/'
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

RECIPIENT_CHAT_ID = os.getenv("RECIPIENT_CHAT_ID")
ACESS_ID = os.getenv("ACESS_ID")

MONGODB_URL = os.getenv("MONGODB_URL")
