import os
import sys
import django
import re
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from asgiref.sync import sync_to_async
from django.utils.timezone import localtime

# ✅ Настройка Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flowerdelivery.settings")
django.setup()  # <-- ВАЖНО: Оставляем только здесь!

# ✅ Импорт моделей Django ПОСЛЕ `setup()`
from orders.models import Order, CustomUser, Profile
from bot.bot_instance import bot, TOKEN

async def start(update: Update, context: CallbackContext):
    """Запрос номера телефона"""
    button = KeyboardButton("📞 Send my phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome to FlowerDelivery bot! To receive order updates, please share your phone number.",
        reply_markup=reply_markup
    )

async def register(update: Update, context: CallbackContext):
    """Регистрирует Telegram ID пользователя"""
    user = update.message.from_user
    contact = update.message.contact

    if not contact:
        await update.message.reply_text("Please share your phone number to register.")
        return

    phone_number = re.sub(r'\D', '', contact.phone_number)
    phone_number = "+7" + phone_number[-10:]

    print(f"Searching for phone number: {phone_number}")

    try:
        user_obj = await sync_to_async(CustomUser.objects.get)(phone_number=phone_number)

        profile, created = await sync_to_async(Profile.objects.get_or_create)(user=user_obj)
        profile.phone_number = phone_number
        profile.telegram_id = user.id
        await sync_to_async(profile.save)()

        await update.message.reply_text("Your Telegram account is linked successfully! You will receive order updates.")

    except CustomUser.DoesNotExist:
        await update.message.reply_text("Your phone number is not registered on our website. Please check your account.")

def main():
    """Запуск бота"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.CONTACT, register))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
