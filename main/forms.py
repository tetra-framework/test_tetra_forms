from django import forms

from main.models import Person, Book


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
