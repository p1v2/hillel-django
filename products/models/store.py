from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=255)
    number_of_employees = models.CharField()
    description = models.TextField(blank=True)
    date_joined = models.DateField()
    address = models.CharField(max_length=80)
    job_title = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=32)



    def __str__(self):
        return self.name