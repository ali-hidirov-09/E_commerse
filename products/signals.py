from django.conf import settings
from .models import Order
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        token = settings.TELEGRAM_BOT_TOKEN
        method =  'sendMessage'

        message_text = (f'New order: {instance.id}\nProduct: {instance.product.name}\nQuantity: {instance.quantity}\n'
                        f'Client: {instance.customer.username}\ntel: {instance.phone_number}')
        response = requests.post(
            url=f"https://api.telegram.org/bot{token}/{method}",
            data={'chat_id': os.environ.get('ADMIN_ID'), 'text':message_text}
        ).json()

