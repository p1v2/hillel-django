from django.contrib.auth.models import User
from django.test import TestCase

from products.models import Order, Product, OrderProduct


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test")
        self.order = Order.objects.create(user=self.user)

    def test_bill(self):
        product = Product.objects.create(name="Coca cola", price=100)
        OrderProduct.objects.create(order=self.order,
                                    product=product, quantity=2)

        product = Product.objects.create(name="Pepsi", price=200)
        OrderProduct.objects.create(order=self.order,
                                    product=product, quantity=3)

        expected_bill = """Coca cola - 2 - 200
Pepsi - 3 - 600
Total: 800"""

        actual_bill = self.order.bill

        self.assertEqual(expected_bill, actual_bill)

    def test_bill_without_products(self):
        expected_bill = """Total: 0"""

        actual_bill = self.order.bill

        self.assertEqual(expected_bill, actual_bill)
