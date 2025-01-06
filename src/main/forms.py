from django import forms

from main.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    terms_conditions = forms.BooleanField(
        required=False, label="I agree to the terms and conditions."
    )


class Person2Form(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    attachment = forms.FileField()
    terms_conditions = forms.BooleanField()
