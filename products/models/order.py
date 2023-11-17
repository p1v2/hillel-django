from django.db import models


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', through='products.OrderProduct')
