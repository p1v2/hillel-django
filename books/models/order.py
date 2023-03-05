
from celery import shared_task
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.telegram import send_telegram_message
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


@receiver(post_save, sender=Order)
def on_order_save_in_thread(sender, instance: Order, created, **kwargs):
    if created:
        on_order_save.delay(instance.id)


@shared_task(autoretry_for=(BaseException,), retry_backoff=2)
def on_order_save(order_id):
    # if random() < 1:
    #     print("The task will be retried in some time...")
    #     raise ValueError("Some error occurred")

    instance = Order.objects.get(id=order_id)

    text = f"""
ORDER {instance.id} CREATED.
Phone: {instance.customer.phone_number}
"""

    for line_item in instance.line_items.all():
        text += f"{line_item.book.name} - {line_item.quantity}\n"

    print("Sending telegram message...")
    send_telegram_message(text)
