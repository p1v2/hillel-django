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


@app.task(bind=True)
def google_sheet_task(self, order_id):
    order = Order.objects.prefetch_related('products').select_related('user').get(id=order_id)

    data = []
    for order_product in order.order_products.all():
        # Make like this: ["Coca cola - 2 - 200", "Total: 200"]
        data.append(f'{order_product.product.name} - {order_product.quantity} - {round(order_product.product.price * order_product.quantity)}')
        data.append(f'Total: {round(order.total_price)}')

    write_to_sheet(data)
