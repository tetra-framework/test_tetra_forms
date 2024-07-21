from django.db import models
from django.db.models import IntegerChoices


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to="files/", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class PersonAddress(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street} ({self.person})"


class Color(IntegerChoices):
    RED = "1"
    BLUE = "2"
    GREEN = "3"


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    delivery_from = models.ForeignKey(
        PersonAddress, on_delete=models.CASCADE, blank=True, null=True
    )
    color = models.IntegerField(choices=Color.choices, default=Color.RED)

    def __str__(self):
        return f"{self.name} ({self.author}, {self.color})"
