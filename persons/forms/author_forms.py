from django import forms

from .person_forms import PersonForm

class AuthorForm(PersonForm):
    alias = forms.CharField(max_length=100)

    class Meta(PersonForm.Meta):
        fields = PersonForm.Meta.fields + ['alias']