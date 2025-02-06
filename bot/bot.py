from telegram import Update, Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
import sys

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flowerdelivery.settings")  # Проверь название проекта!
django.setup()

from orders.models import Order
from django.contrib.auth.models import User

TOKEN = '7691200173:AAHmGl9Q3iXjddPohx3jleGowFsUwiUrSAw'
bot = Bot(token=TOKEN)

async def start(update: Update, context: CallbackContext):
    """Приветственное сообщение и запрос номера телефона."""
    button = KeyboardButton("📞 Send my phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome to FlowerDelivery bot! To receive order updates, please share your phone number.",
        reply_markup=reply_markup
    )

async def register(update: Update, context: CallbackContext):
    """Регистрация Telegram ID через номер телефона."""
    user = update.message.from_user
    contact = update.message.contact

    if not contact:
        await update.message.reply_text("Please share your phone number to register.")
        return

    phone_number = contact.phone_number

    try:
        user_obj = User.objects.get(profile__phone_number=phone_number)
        user_obj.profile.telegram_id = user.id  # Привязываем Telegram ID к пользователю
        user_obj.profile.save()
        await update.message.reply_text("Your Telegram account is linked successfully! You will receive order updates.")
    except User.DoesNotExist:
        await update.message.reply_text("Your phone number is not registered on our website. Please check your account.")

async def order_status(update: Update, context: CallbackContext):
    """Получение статуса заказов пользователя."""
    user = update.message.from_user
    orders = Order.objects.filter(user__profile__telegram_id=user.id)

    if orders.exists():
        message = '\n'.join([f"Order #{order.id} - {order.status}" for order in orders])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text('No orders found.')

def send_order_notification(order):
    """Отправка уведомления пользователю о новом заказе."""
    if order.user.profile.telegram_id:
        message = (
            f"Your bouquet \"{order.bouquet.name}\" will be delivered on {order.delivery_date} "
            f"from {order.delivery_time}. \nOrder status: {order.status}."
        )
        bot.send_message(chat_id=order.user.profile.telegram_id, text=message)

def main():
    """Запуск бота."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.CONTACT, register))
    app.add_handler(CommandHandler('status', order_status))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()