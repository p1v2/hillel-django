import datetime as dt
from django.core.mail import EmailMessage

from google_sheets.client import write_to_sheet
from hillel_django.celery import app
from products.models import Order, Product



@app.task(bind=True)
def order_created_task(self, order_id):
    order = (
        Order.objects.prefetch_related("products")
        .select_related("user")
        .get(id=order_id)
    )

    message = f"Order {order_id} created!\n"

    for order_product in order.order_products.all():
        message += f"{order_product.product.name} - {order_product.quantity}\n"

    message += f"User: {order.user.email}"

    html_message = f"""
    <h1>Order {order_id} created!</h1>
    <ul>
    """

    for order_product in order.order_products.all():
        html_message += (
            f"<li>{order_product.product.name} - {order_product.quantity}</li>"
        )

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
    message.attach(
        "person.jpeg",
        open("person.jpeg", "rb").read(),
        "image/jpeg"
    )
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
    order = (
        Order.objects.prefetch_related("products")
        .select_related("user")
        .get(id=order_id)
    )

    data = []
    for order_product in order.order_products.all():
        # Make like this: ["Coca cola - 2 - 200", "Total: 200"]
        data.append(
            f"{order_product.product.name} - "
            f"{order_product.quantity} - "
            f"{round(order_product.product.price * order_product.quantity)}"
        )
        data.append(f"Total: {round(order.total_price)}")

    write_to_sheet(data)


@app.task(bind=True)
def daily_stats(self):
    day_before = dt.date.today() - dt.timedelta(days=1)
    orders = Order.objects.filter(created_on=day_before)
    order_count = orders.count()

    print(f"Number of orders during {day_before}: {order_count}")

    if order_count > 0:
        product_quantity = {}
        for order in orders:
            for order_product in order.order_products.all():
                product_id = order_product.product_id
                if product_id in product_quantity:
                    product_quantity[product_id] += order_product.quantity
                else:
                    product_quantity[product_id] = order_product.quantity
        list_product_quantity = list(product_quantity.items())
        list_product_quantity.sort(reverse=True, key=lambda x: x[1])
        top3 = list_product_quantity[:3]
        
        for id, quantity in top3:
            product = Product.objects.get(id=id)
            print(f"{product.name} {quantity}")
