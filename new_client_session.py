import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")

# Авторизация и печать ключа сессии
with TelegramClient(StringSession(), int(api_id), api_hash) as client:
    print(client.session.save())