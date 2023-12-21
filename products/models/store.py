from django.db import models

class Store(models.Model):
        name = models.CharField(max_length=255, unique=True)
        location = models.CharField()
        opening_hours = models.CharField()
        products = models.ManyToManyField('products.Product', through='products.StoreInventory')

        def __str__(self):
            return self.name