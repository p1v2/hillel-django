from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from products import models
from products.models import Order
import logging


@shared_task
def gather_and_log_order_statistics():
    end_date = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=1)

    orders_count = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date).count()

    top_products = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date) \
                       .values('product').annotate(product_count=models.Count('product')).order_by('-product_count')[:3]

    logging.info(f"Statistics for {start_date} to {end_date}:")
    logging.info(f"Total orders created: {orders_count}")
    logging.info("Top 3 ordered products:")
    for product in top_products:
        logging.info(f"Product: {product['product']}, Count: {product['product_count']}")
