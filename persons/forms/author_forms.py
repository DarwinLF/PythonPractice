from django import forms

from .person_forms import PersonForm
from ..models import Author

class AuthorForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Author
        fields = PersonForm.Meta.fields + ['alias']
        widgets = {
            **PersonForm.Meta.widgets,
            'alias': forms.TextInput(attrs={'class': 'form-control'}),
        }