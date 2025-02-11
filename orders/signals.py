from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
# from bot.bot import send_order_notification  # Импортируем функцию отправки уведомлений
def notify_order_created(order):
    from bot.bot import send_order_notification  # Перемещаем импорт внутрь функции
    send_order_notification(order)

@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, **kwargs):
    """Отправка уведомления при изменении статуса заказа."""
    if instance.pk:  # Проверяем, что заказ уже существует в базе
        previous_order = Order.objects.filter(pk=instance.pk).first()
        if previous_order and previous_order.status != instance.status:
            from bot.bot import send_order_notification
            send_order_notification(instance)