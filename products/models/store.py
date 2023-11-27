from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField()
    opening_hours = models.CharField()
    description = models.TextField(blank=True)
    products = models.ManyToManyField('products.Product', through='products.StoreInventory')

    def __str__(self):
        return self.name