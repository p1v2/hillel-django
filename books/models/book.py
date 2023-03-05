from django.contrib.auth.models import User
from django.db import models

from books.models import Author
from books.models import Country


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    count_sold = models.IntegerField(default=0)

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)

    def __str__(self):
        return f'{self.name} {self.authors} {self.pages_count} {self.country} {self.seller} {self.price}'

    def get_information(self):
        author_info = {
            'first_name': Author.first_name,
            'last_name': Author.last_name,
        }
        book_info = {
            'name': self.name,
            'authors': self.authors,
            'pages_count': self.pages_count,
            'country': self.country,
            'seller': self.seller,
            'info_about_authors': author_info,
            'price': self.price,
        }

        return book_info
