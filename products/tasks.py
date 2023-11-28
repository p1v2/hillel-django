from django.core.mail import EmailMessage

from google_sheets.client import write_to_sheet
from hillel_django.celery import app
from products.models import Order, Product


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
def every_minute_task(self):
    products = Product.objects.all()

    product_data = []

    for product in products:
        product_data.append([product.id, product.name, product.price])

    write_to_sheet(product_data)

    return "Done!"
