from django.db import models


class StoreInventory(models.Model):
    market = models.ForeignKey('products.market', on_delete=models.CASCADE)
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    count_of_product = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.market}"

