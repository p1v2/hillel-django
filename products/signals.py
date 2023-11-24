from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Order
from products.tasks import order_created_task


@receiver(post_save, sender=Order)
def order_created(sender, instance, **kwargs):
    order_created_task.apply_async(args=(instance.id,))
