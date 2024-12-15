from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from orders.models import Order

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to FlowerDelivery bot!')

def order_status(update: Update, context: CallbackContext):
    user = update.message.from_user
    orders = Order.objects.filter(user__username=user.username)
    if orders.exists():
        message = '\n'.join([f"Order #{order.id} - {order.status}" for order in orders])
        update.message.reply_text(message)
    else:
        update.message.reply_text('No orders found.')

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('status', order_status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()