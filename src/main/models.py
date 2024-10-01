from django.db import models
from django.db.models import IntegerChoices


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to="files/", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
