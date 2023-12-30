from django import forms

from .person_forms import PersonForm
from ..models import Customer

class CustomerForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Customer
        fields = PersonForm.Meta.fields + ['library']
        widgets = {
            **PersonForm.Meta.widgets,
            'library': forms.Select(attrs={'class': 'form-control'}),
        }