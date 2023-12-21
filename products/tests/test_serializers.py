from django.test import TestCase

from django.contrib.auth.models import User

from products.models import Order, OrderProduct, Product
from products.serializers import OrderSerializer


class SerializersTestCase(TestCase):
    def test_order_get_products_count_no_products(self):
        user = User.objects.create(username="test")
        order = Order.objects.create(user=user)

        serializer = OrderSerializer(order)

        self.assertEqual(0, serializer.data["products_count"])

    def test_order_get_products_count(self):
        user = User.objects.create(username="test")
        order = Order.objects.create(user=user)

        cola = Product.objects.create(name="Coca cola", price=100)
        pepsi = Product.objects.create(name="Pepsi", price=200)

        OrderProduct.objects.create(order=order, product=cola, quantity=2)
        OrderProduct.objects.create(order=order, product=pepsi, quantity=3)

        serializer = OrderSerializer(order)

        self.assertEqual(2, serializer.data["products_count"])
