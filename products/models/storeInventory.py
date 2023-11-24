from django.db import models
from django.db.models import Count


from products.models.product import Product
from products.models.store import Store

class StoreInventory(models.Model):
        name = models.CharField(max_length=255)
        store = models.ForeignKey(Store, on_delete=models.CASCADE)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        description = models.TextField(blank=True)
        quantity = models.IntegerField()  # Stock count for the product in a specific store

        class Meta:
            unique_together = ('store', 'product')  # Ensuring each store-product combo is unique.

        def __str__(self):
            return f"{self.store.name} - {self.product.name} ({self.quantity})"
