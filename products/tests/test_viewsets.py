from django.contrib.auth.models import User
from django.test import TestCase

from products.models import Product, Order


class ViewsetsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test")
        self.client.force_login(self.user)

    def test_create_order(self):
        cola = Product.objects.create(name="Coca cola", price=100)
        pepsi = Product.objects.create(name="Pepsi", price=200)

        response = self.client.post(
            "/api/orders/",
            data={
                "order_products": [
                    {"product": cola.id, "quantity": 2},
                    {"product": pepsi.id, "quantity": 3},
                ]
            },
            content_type="application/json",
        )

        self.assertEqual(201, response.status_code)

        order = Order.objects.first()
        self.assertEqual(2, order.order_products.count())
        self.assertEqual(self.user, order.user)

        order_products = order.order_products.all()

        self.assertEqual(order_products.get(product=cola).quantity, 2)
        self.assertEqual(order_products.get(product=pepsi).quantity, 3)

    def test_create_order_without_products(self):
        response = self.client.post(
            "/api/orders/",
            data={"order_products": []},
            content_type="application/json"
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "You must specify at least one product",
            response.json()["non_field_errors"][0],
        )
