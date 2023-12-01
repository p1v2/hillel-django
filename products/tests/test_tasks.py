from django.test import TestCase
from unittest.mock import patch

from django.contrib.auth.models import User

from products.models import Order, Product, OrderProduct
from products.tasks import google_sheet_task


class TaskTestCase(TestCase):
    @patch('products.tasks.write_to_sheet')
    def test_google_sheet_task(self, write_to_sheet):
        user = User.objects.create(username='test')
        order = Order.objects.create(user=user)

        cola = Product.objects.create(name='Coca cola', price=100)
        OrderProduct.objects.create(order=order, product=cola, quantity=2)

        google_sheet_task(order.id)

        write_to_sheet.assert_called_once_with(["Coca cola - 2 - 200", "Total: 200"])
