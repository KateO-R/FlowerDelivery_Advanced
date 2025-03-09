from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from bot.tasks import send_order_notification
from asgiref.sync import sync_to_async
from .models import Order

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    """Отправка уведомления при изменении статуса заказа"""
    if instance.pk:
        try:
            previous_status = Order.objects.get(pk=instance.pk).status
            if previous_status != instance.status:
                sync_to_async(send_order_notification)(instance)
        except ObjectDoesNotExist:
            pass