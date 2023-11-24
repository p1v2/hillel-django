from django.db import models


class StoreInventory(models.Model):
    store = models.ForeignKey('undefApp.Store', on_delete=models.CASCADE)
    product = models.ForeignKey('undefApp.Product', on_delete=models.CASCADE)
    exclusive_features = models.TextField(blank=True)
    amount = models.PositiveIntegerField(default=0)   

    def __str__(self):
        return f'{self.product.name} ({self.store})'