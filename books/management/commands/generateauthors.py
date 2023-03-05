from django.core.management import BaseCommand

from faker import Faker

from books.models import Book, Author

fake = Faker(locale="uk")


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()

            Author.objects.create(first_name=first_name, last_name=last_name)

        for book in Book.objects.all():
            book.authors.add(
                Author.objects.order_by('?').first()
            )
