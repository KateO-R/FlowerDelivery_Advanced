print("ЗАГРУЗКА bot_instance.py")
from telegram import Bot
import os

def get_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "7691200173:AAHmGl9Q3iXjddPohx3jleGowFsUwiUrSAw")
    return Bot(token=token)