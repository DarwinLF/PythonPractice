from django import forms

from datetime import date

from ..models import Rent

class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['book', 'customer', 'employee', 'library',
                   'due_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'library': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        data = self.cleaned_data
        due_date = data['due_date']

        if due_date < date.today():
            self.add_error('due_date', 'The due date can\'t be in the past')
        
        return data