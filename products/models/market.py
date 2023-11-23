from django.db import models

class Market(models.Model):
    name = models.CharField(max_length=255)
    working_data= models.DateField()
    is_open = models.BooleanField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name