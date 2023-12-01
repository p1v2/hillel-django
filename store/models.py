# from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone
# from django.core.exceptions import ValidationError
from products.models import Product


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    established = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    # location = gis_models.PointField(null=True, blank=True)
    opening_hours = models.CharField(max_length=255)
    manager_id = models.TextField(blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    floor_space = models.FloatField()
    employees = models.IntegerField()

    products = models.ManyToManyField(
        'products.Product',
        through='StoreInventory',
        through_fields=('store', 'product'),
    )

    def __str__(self):
        return self.name


class StoreInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier_id = models.IntegerField()
    good_until = models.DateField()


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.FloatField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    store_inventory = models.ForeignKey(StoreInventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


# Create your models here.
