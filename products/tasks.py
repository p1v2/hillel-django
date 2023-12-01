from time import sleep

from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.db.models import Sum

from hillel_django.mycelery import app
from products.models import Order, OrderProduct
# from telegram.client import send_message
from datetime import datetime, timedelta

@app.task(bind=True)
def order_created_task(self, order_id):
    # order = Order.objects.prefetch_related('products').select_related('user').get(id=order_id)

    # message = f'Order {order_id} created!\n'

    # for order_product in order.order_products.all():
    #     message += f'{order_product.product.name} - {order_product.quantity}\n'

    # message += f'User: {order.user.email}'
    pass
    # send_message(message)
    # Send raw text email
    # send_mail(
    #     "New Order",
    #     message,
    #     "pavliuk96@gmail.com",
    #     [order.user.email],
    # )

    # html_message = f"""
    # <h1>Order {order_id} created!</h1>
    # <ul>
    # """

    # for order_product in order.order_products.all():
    #     html_message += f'<li>{order_product.product.name} - {order_product.quantity}</li>'

    # html_message += f"""
    # </ul>
    # <p>User: {order.user.email}</p>
    # """

    # Send html email
    # send_mail(
    #     "New Order",
    #     message,
    #     "pavliuk96@gmail.com",
    #     [order.user.email],
    #     html_message=html_message,
    # )

    # Send email with attachment
    # message = EmailMessage(
    #     "New Order",
    #     message,
    #     "pavliuk96@gmail.com",
    #     [order.user.email],
    # )
    # message.attach('person.jpeg', open('person.jpeg', 'rb').read(), 'image/jpeg')
    # message.send()


@app.task(bind=True)
def every_second_task(self):
    print("Start every second task!")
    sleep(10)
    print('End every second task!')


@app.task(bind=True)
def daily_order_check(self):
    yesterday = datetime.now() - timedelta(days=1,seconds=1)

    yesterday_orders = OrderProduct.objects.select_related('product','order').filter(order__created_at__range=(yesterday, datetime.now()))
    ordercount = yesterday_orders.count()

    message = f"It's your daily checkout of orders!\n{ordercount} orders were created yesterday.\nTop 3 bestsellers were:\n"
    
    top_orders = yesterday_orders.values('product__name').annotate(units=Sum('quantity')).order_by('-units')[:3]
    for order in top_orders:
        message += f'{order["product__name"]} - {order["units"]} units;\n'
    print(message)
    # print(
    #       The top 3 products were:
    #         'order.name1';
    #         'order.name2'
    #         'order.name3'""")