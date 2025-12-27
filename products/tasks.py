from django.conf import settings
import requests
import time
from celery import shared_task
import os

@shared_task()
def send_telegram_notifications(order_id, product_name, customer_username, phone_number, quantity):
    time.sleep(5)
    token = settings.TELEGRAM_BOT_TOKEN
    method =  'sendMessage'
    message_text = (f'New order: {order_id}\nProduct: {product_name}\nQuantity: {quantity}\n'
                    f'Client: {customer_username}\ntel: {phone_number}')
    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/{method}",
        data={'chat_id': os.environ.get('ADMIN_ID'), 'text':message_text}
    ).json()
