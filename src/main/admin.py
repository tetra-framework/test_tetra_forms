from django.contrib import admin

from main.models import Person, Book, PersonAddress

admin.site.register(Person)
admin.site.register(Book)
admin.site.register(PersonAddress)
