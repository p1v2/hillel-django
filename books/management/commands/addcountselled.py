#3) Додати команду python manage.py addcountselled
# яка до кожної книжки додаватиме випадкове число в новоствореному полі count_selled.
from django.core.management import BaseCommand
from random import randint
from books.models import Book

class Command(BaseCommand):
    def handle(self, *args, **options):

        for book in Book.objects.all():
            count_selled = randint(100, 200)
            # country = random.choice(countries)

            book.count_selled = count_selled
            book.save()
