from django.db import models
from products.models.store import Store

from products.models.product import Product


class StoreInventory(models.Model):
    store = models.ForeignKey("products.Store", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.store.name}  -  {self.product.name} x {self.quantity}'