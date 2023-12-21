from django.db import models


class OrderProduct(models.Model):
    order = models.ForeignKey(
        "products.Order", on_delete=models.CASCADE,
        related_name="order_products"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE,
        related_name="order_products"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
