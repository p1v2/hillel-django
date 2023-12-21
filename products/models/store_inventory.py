from django.db import models


class StoreInventory(models.Model):
    store = models.ForeignKey('products.Store', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.product.name} x {self.quantity}'