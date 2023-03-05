from django.core.management import BaseCommand
from random import randint
from books.models import Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        for book in Book.objects.all():
            count_selled = randint(1, 1000)
            book.count_selled = count_selled
            book.save()