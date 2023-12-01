from time import sleep

from django.core.mail import send_mail, EmailMessage

from hillel_django.mycelery import app
from products.models import Order
# from telegram.client import send_message


@app.task(bind=True)
def order_created_task(self, order_id):
    order = Order.objects.prefetch_related('products').select_related('user').get(id=order_id)

    message = f'Order {order_id} created!\n'

    for order_product in order.order_products.all():
        message += f'{order_product.product.name} - {order_product.quantity}\n'

    message += f'User: {order.user.email}'

    # send_message(message)
    # Send raw text email
    # send_mail(
    #     "New Order",
    #     message,
    #     "pavliuk96@gmail.com",
    #     [order.user.email],
    # )

    html_message = f"""
    <h1>Order {order_id} created!</h1>
    <ul>
    """

    for order_product in order.order_products.all():
        html_message += f'<li>{order_product.product.name} - {order_product.quantity}</li>'

    html_message += f"""
    </ul>
    <p>User: {order.user.email}</p>
    """

    # Send html email
    # send_mail(
    #     "New Order",
    #     message,
    #     "pavliuk96@gmail.com",
    #     [order.user.email],
    #     html_message=html_message,
    # )

    # Send email with attachment
    message = EmailMessage(
        "New Order",
        message,
        "pavliuk96@gmail.com",
        [order.user.email],
    )
    message.attach('person.jpeg', open('person.jpeg', 'rb').read(), 'image/jpeg')
    message.send()


@app.task(bind=True)
def every_second_task(self):
    print("Start every second task!")
    sleep(10)
    print('End every second task!')


@app.task(bind=True)
def daily_order_check(self):
    for order in Order.objects.all().prefetch_related('products'):
        print(order.created_at)
    # print(f"""It's your daily checkout of orders!
    #       1 orders were created yesterday.
    #       The top 3 products were:
    #         'order.name1';
    #         'order.name2'
    #         'order.name3'""")