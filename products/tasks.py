from time import sleep

from hillel_django.celery import app
from products.models import Order
from telegram.client import send_message


@app.task(bind=True)
def order_created_task(self, order_id):
    order = Order.objects.prefetch_related('products').select_related('user').get(id=order_id)

    message = f'Order {order_id} created!\n'

    for order_product in order.order_products.all():
        message += f'{order_product.product.name} - {order_product.quantity}\n'

    message += f'User: {order.user.email}'

    send_message(message)


@app.task(bind=True)
def every_second_task(self):
    print("Start every second task!")
    sleep(10)
    print('End every second task!')

