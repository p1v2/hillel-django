import random

import factory
from django.core.management import BaseCommand
from factory.django import DjangoModelFactory
from faker import Faker

from products.models import Product, Category

fake = Faker()


def insert_products(products):
    for product in products:
        category_name = product['category']
        category, _ = Category.objects.get_or_create(name=category_name)

        Product.objects.create(
            name=product['name'],
            price=product['price'],
            description=product['description'],
            category=category
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Generate categories
        categories = [fake.unique.word() for _ in range(10)]

        # Generate products
        products = []
        for _ in range(100):
            product_name = fake.unique.word()
            category_name = random.choice(categories)
            products.append({
                'name': product_name,
                'price': round(random.uniform(10, 500), 2),
                'description': fake.text(),
                'category': category_name
            })

        # products now contains 100 product dictionaries
        insert_products(products)
