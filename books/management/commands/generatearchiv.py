import random

from django.core.management import BaseCommand

from books.models import Country, Book


class Command(BaseCommand):
    def handle(self, *args, **options):

        for book in Book.objects.all():
            is_archived = random.choice([True, False])

            book.is_archived = is_archived
            book.save()
