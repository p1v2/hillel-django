from django.db import models
from rest_framework.authtoken.admin import User


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=40, unique=True)
    pages_count = models.IntegerField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    count_selled = models.IntegerField(null=True)
    is_archived = models.BooleanField(null=True)

    @property
    def authors_string(self):
        authors_names = []

        for author in self.authors.all():
            authors_names.append(f"{author.first_name} {author.last_name}")

        return ", ".join(authors_names)


    def __str__(self):
        return self.name
