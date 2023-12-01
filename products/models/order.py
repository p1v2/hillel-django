from django.db import models
from datetime import datetime


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', through='products.OrderProduct')
    created_at = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return f'{self.user} at {self.created_at.hour}:{self.created_at.minute}, {self.created_at.date()}'