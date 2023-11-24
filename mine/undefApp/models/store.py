from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # models.CASCADE - if category is deleted, all products in this category will be deleted
    # models.SET_NULL - if category is deleted, all products in this category will be set to NULL
    # models.RESTRICT - don't allow to delete category if there are products in this category
    # models.DO_NOTHING - don't do anything if category is deleted
    products = models.ManyToManyField('undefApp.Product', through='undefApp.StoreInventory')
    
    def __str__(self) -> str:
        return self.name