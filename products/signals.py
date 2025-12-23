from django.conf import settings
from .models import Order
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        token = settings.TELEGRAM_BOT_TOKEN
        method =  'sendMessage'

        message_text = (f'New order: {instance.id}\n Product: {instance.product.name}\n Quantity: {instance.quantity}'
                        f'Client: {instance.customer.usrename}\n tel: {instance.phone_number}')
        response = requests.post(
            url=f"https://api.telegram.org/bot{token}/{method}",
            data={'chat_id': 7260643230, 'text':message_text}
        ).json()

