from bot.bot_instance import bot
from asgiref.sync import sync_to_async

async def send_order_notification(order):
    """Отправляет уведомление пользователю при изменении статуса заказа"""
    if order.user.profile.telegram_id:
        bouquets = ", ".join([item.product.name for item in order.orderproduct_set.all()])

        message = (
            f"🌸 Your order #{order.id} has been updated!\n"
            f"📅 Delivery date: {order.delivery_date}\n"
            f"⏰ Time: {order.time}\n"
            f"💐 Bouquets: {bouquets}\n"
            f"📦 Status: {order.get_status_display()}\n"
        )

        await bot.send_message(chat_id=order.user.profile.telegram_id, text=message)
