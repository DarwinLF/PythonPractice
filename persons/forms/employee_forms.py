from django import forms

from .person_forms import PersonForm
from ..models import Employee

class EmployeeForm(PersonForm):
    class Meta(PersonForm.Meta):
        model = Employee
        fields = PersonForm.Meta.fields + ['library']
        widgets = {
            **PersonForm.Meta.widgets,
            'library': forms.Select(attrs={'class': 'form-control'}),
        }