from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Order, OrderProduct, Profile
from bot.bot_instance import get_bot
import telegram.error
import asyncio

print("✅ bot.tasks загружен!")

# 🔍 Глобальный словарь для хранения старых статусов перед изменением
OLD_STATUSES = {}

@receiver(pre_save, sender=Order)
def store_old_status(sender, instance, **kwargs):
    """Сохраняем старый статус перед изменением"""
    try:
        OLD_STATUSES[instance.pk] = Order.objects.get(pk=instance.pk).status
    except Order.DoesNotExist:
        OLD_STATUSES[instance.pk] = None

@receiver(post_save, sender=OrderProduct)
def order_product_saved(sender, instance, **kwargs):
    """Отправляем уведомление после сохранения всех товаров"""
    print(f"🛍 OrderProduct saved! Checking if all items are ready for Order #{instance.order.id}...")

    # Ждем 2 секунды для надежности
    async_to_sync(asyncio.sleep)(2)

    # Запускаем отправку уведомления для заказа
    async_to_sync(send_order_notification)(instance.order)

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    """Отправка уведомления при изменении статуса заказа"""
    old_status = OLD_STATUSES.get(instance.pk)

    print(f"🔔 Signal post_save triggered! Order #{instance.id}")
    print(f"ℹ️ Previous status: {old_status}")
    print(f"ℹ️ New status (instance): {instance.status}")

    # Для нового заказа ждем OrderProduct
    if created:
        print(f"🕒 Order just created, waiting for products...")
        return  # ⚠️ Не отправляем уведомление сразу!

    if old_status != instance.status:
        print(f"🚀 Calling send_order_notification for order #{instance.id}")
        async_to_sync(send_order_notification)(instance)
    else:
        print(f"⚠️ Order status has not changed. Notification not sent.")

async def send_order_notification(order):
    """Sends a notification to the user when the order status changes"""

    print(f"📨 Attempting to send notification for order #{order.id}")

    # 🔹 Получаем профиль пользователя асинхронно
    profile = await sync_to_async(Profile.objects.filter(user=order.user).first)()

    if not profile or not profile.telegram_id:
        print(f"⚠️ No Telegram ID found for user {order.user}")
        return

    # 🔹 Ждем 1 секунду перед загрузкой товаров (на случай задержки БД)
    await asyncio.sleep(1)

    # 🔹 Получаем список товаров в заказе асинхронно
    order_products = await sync_to_async(list)(OrderProduct.objects.filter(order=order).select_related("product"))
    bouquets = ", ".join([item.product.name for item in order_products]) if order_products else "No products listed"

    message = (
        f"🌸 <b>Your order #{order.id} has been updated!</b>\n"
        f"📅 <b>Delivery Date:</b> {order.delivery_date}\n"
        f"⏰ <b>Time:</b> {order.time}\n"
        f"💐 <b>Bouquets:</b> {bouquets}\n"
        f"📦 <b>Status:</b> {order.get_status_display()}\n"
    )

    bot = get_bot()
    try:
        await bot.send_message(chat_id=profile.telegram_id, text=message, parse_mode="HTML")
        print(f"✅ Notification sent to user {profile.telegram_id} for order #{order.id}")
    except telegram.error.TelegramError as e:
        print(f"❌ Error sending notification: {e}")
