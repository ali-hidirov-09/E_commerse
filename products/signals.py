from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_telegram_notifications

@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        send_telegram_notifications.delay(
            order_id=instance.id,
            product_name=instance.product.name,
            customer_username=instance.customer.phone_number,
            phone_number=instance.phone_number,
            quantity=instance.quantity,
        )

