# Create your models here.
from django.core.exceptions import ValidationError
from django.db import models

from products.models.category import Category
from products.models.tag import Tag


def non_negative_validator(value):
    if value <= 0:
        raise ValidationError('Price cannot be negative.')


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[non_negative_validator])
    description = models.TextField(blank=True)
    # models.CASCADE - if category is deleted, all products in this category will be deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    # models.SET_NULL - if category is deleted, all products in this category will be set to NULL
    # models.RESTRICT - don't allow to delete category if there are products in this category
    # models.DO_NOTHING - don't do anything if category is deleted
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    orders = models.ManyToManyField('products.Order', through='products.OrderProduct')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name