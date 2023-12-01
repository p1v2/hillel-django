from celery import shared_task
from django.db.models import Count
from store.models import Order, OrderItem
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def collect_daily_order_stats():
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)

    # Count how many orders were created during the last day
    order_count = Order.objects.filter(order_date__date=yesterday).count()
    logger.info(f'Number of orders created yesterday: {order_count}')

    # Identify the top 3 ordered products
    top_products = (OrderItem.objects.filter(order__order_date__date=yesterday)
                    .values('store_inventory__product__name')
                    .annotate(total_ordered=Count('store_inventory__product'))
                    .order_by('-total_ordered')[:3])

    for product in top_products:
        logger.info(f'Product: {product["store_inventory__product__name"]}, Quantity: {product["total_ordered"]}')
