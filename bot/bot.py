from telegram import Update, Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
import sys
import re
from django.utils.translation import gettext_lazy as _
from asgiref.sync import sync_to_async

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flowerdelivery.settings")  # Проверь название проекта!
django.setup()

from orders.models import Order, Profile
from django.contrib.auth import get_user_model

User = get_user_model()
TOKEN = '7691200173:AAHmGl9Q3iXjddPohx3jleGowFsUwiUrSAw'
bot = Bot(token=TOKEN)


async def start(update: Update, context: CallbackContext):
    """Sends a welcome message and requests the user's phone number."""
    button = KeyboardButton("📞 Send my phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome to FlowerDelivery bot! To receive order updates, please share your phone number.",
        reply_markup=reply_markup
    )


async def register(update: Update, context: CallbackContext):
    """Registers the user's Telegram ID using their phone number."""
    user = update.message.from_user
    contact = update.message.contact

    if not contact:
        await update.message.reply_text("Please share your phone number to register.")
        return

    phone_number = re.sub(r'\D', '', contact.phone_number)  # Удаляем пробелы и нецифровые символы
    if phone_number.startswith("7"):
        phone_number = "+7" + phone_number[1:]

    elif phone_number.startswith("8"):
        phone_number = "+7" + phone_number[1:]

    elif len(phone_number) == 10:  # Если пришли только 10 цифр (например, "9028789229"), добавляем "+7"
        phone_number = "+7" + phone_number

    print(f"Searching for phone number: {phone_number}")

    try:
        user_obj = await sync_to_async(User.objects.select_related("profile").get)(profile__phone_number=phone_number)

        if not hasattr(user_obj, "profile"):  # Проверяем, есть ли у пользователя профиль
            await update.message.reply_text("Your account is missing a profile. Please contact support.")
            return

        if not user_obj.profile.phone_number:  # Сохраняем номер, если его нет
            user_obj.profile.phone_number = phone_number
            await sync_to_async(user_obj.profile.save)()

        user_obj.profile.telegram_id = user.id  # Link Telegram ID to the user
        await sync_to_async(user_obj.profile.save)()

        await update.message.reply_text("Your Telegram account is linked successfully! You will receive order updates.")
    except User.DoesNotExist:
        await update.message.reply_text("Your phone number is not registered on our website. Please check your account.")


async def order_status(update: Update, context: CallbackContext):
    """Send the user's order status using their linked Telegram ID."""
    user = update.message.from_user

    # Ищем профиль по Telegram ID + загружаем связанную модель User
    try:
        profile = await sync_to_async(Profile.objects.select_related("user").get)(telegram_id=user.id)
    except Profile.DoesNotExist:
        await update.message.reply_text("You are not registered. Please use /start and share your phone number first.")
        return

    # Проверяем, связан ли профиль с пользователем
    if not profile.user:
        await update.message.reply_text("Your profile is not linked to a user account.")
        return

    # Получаем заказы пользователя
    orders = await sync_to_async(list)(Order.objects.filter(user=profile.user))

    if not orders:
        await update.message.reply_text("You have no orders.")
        return

    # Формируем сообщение со статусами заказов
    message = '\n'.join([f"Order #{order.id} - {order.status}" for order in orders])

    await update.message.reply_text(message)


async def send_order_notification(order):
    """Sends a notification to the user about their order status."""
    if order.user.profile.telegram_id:
        message = (
            f"Your bouquet \"{order.bouquet.name}\" will be delivered on {order.delivery_date} "
            f"from {order.delivery_time}. \nOrder status: {order.status}."
        )
        await sync_to_async(bot.send_message)(chat_id=order.user.profile.telegram_id, text=message)


def main():
    """Starts the bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.CONTACT, register))
    app.add_handler(CommandHandler('status', order_status))

    print("Bot is running...")
    app.run_polling()


if __name__ == '__main__':
    main()