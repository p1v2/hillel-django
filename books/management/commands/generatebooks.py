from django.core.management import BaseCommand
from random import randint

from faker import Faker

from books.models import Book

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        books_names_set = set(Book.objects.all().values_list("name", flat=True))

        for _ in range(1000):
            book_name = fake.name()

            if book_name in books_names_set:
                continue

            books_names_set.add(book_name)

            pages_count = randint(1, 1000)
            price = randint(100, 1000)

            book = Book.objects.create(name=book_name, pages_count=pages_count, price=price)
            print(book_name, pages_count)
            print(book.authors_string)
