from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Order
from products.tasks import gather_and_log_order_statistics


@receiver(post_save, sender=Order)
def order_created(sender, instance, **kwargs):
    gather_and_log_order_statistics.apply_async(args=(instance.id,))
