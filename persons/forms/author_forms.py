from django import forms

from .person_forms import PersonForm
from ..models import Author

class AuthorForm(PersonForm):
    alias = forms.CharField(max_length=100)

    class Meta(PersonForm.Meta):
        model = Author
        fields = PersonForm.Meta.fields + ['alias']