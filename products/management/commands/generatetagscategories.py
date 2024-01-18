import random

from django.core.management import BaseCommand

from products.models import Category, Tag, Product


class Command(BaseCommand):
    def execute(self, *args, **options):
        categories_names = [
            "Fruits",
            "Vegetables",
            "Meat",
            "Fish",
            "Milk",
            "Bread",
            "Canned",
            "Sweets",
            "Drinks",
        ]


        categories = []
        for category_name in categories_names:
            # category, true/false
            category, _ = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        tags_names = [
            "Organic",
            "Local",
            "Gluten Free",
            "Lactose Free",
            "Vegan",
            "Vegetarian",
        ]

        tags = []
        for tag_name in tags_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        for product in Product.objects.all():
            # Add random category
            product.category = random.choice(categories)

            # Add random tags
            product.tags.set(random.choices(tags, k=random.randint(1, len(tags))))

            product.save()
