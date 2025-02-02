from telegram import Update
from telegram.ext import CallbackContext
from django.contrib.auth.models import User
from orders.models import Profile

def register(update: Update, context: CallbackContext):
    """Регистрирует Telegram ID пользователя"""
    username = update.message.from_user.username
    telegram_id = update.message.chat_id

    try:
        user = User.objects.get(username=username)
        user.profile.telegram_id = telegram_id
        user.profile.save()
        update.message.reply_text("You have successfully registered your Telegram ID.")
    except User.DoesNotExist:
        update.message.reply_text("User not found. Please check your username in the system.")