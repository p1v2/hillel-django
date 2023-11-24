from time import sleep
import schedule
import time
from collections import Counter
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
def job(self, order_id):
    lst = []
    max_dict = {}
    order = Order.objects.prefetch_related('products').select_related('user').get(id=order_id)

    for order_product in order.order_products.all():
        lst += dict([order_product.product.name,order_product.quantity])

    for order_product in order.order_products.all():
        temp = [i[order_product.product.name] for i in lst]
    for k, v in Counter(temp).items():
        max_dict.update({k:v})

    print(f"The number of orders:{len(lst)},Three coolest orders of the day:{(sorted(max_dict, key=max_dict.get)[-3:])}")

schedule.every().day.at("08:00").do(job)

