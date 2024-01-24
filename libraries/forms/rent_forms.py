from django import forms

from datetime import date

from ..models import Rent

class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['book', 'customer', 'employee', 'library',
                  'amount_to_rent', 'rent_date', 'due_date', 'status']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control', 
                                        'id': 'bookSelect'}),
            'customer': forms.Select(attrs={'class': 'form-control', 
                                            'id': 'customerSelect'}),
            'employee': forms.Select(attrs={'class': 'form-control', 
                                            'id': 'employeeSelect'}),
            'library': forms.Select(attrs={'class': 'form-control', 
                                           'id': 'librarySelect'}),
            'amount_to_rent': forms.NumberInput(attrs=
                                                {'class': 'form-control'}),
            'rent_date': forms.DateInput(attrs={'type': 'date', 
                                                'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 
                                               'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = self.cleaned_data
        book = data['book']
        amount_to_rent = data['amount_to_rent']
        customer = data['customer']
        rent_date = data['rent_date']
        due_date = data['due_date']
        instance_pk = self.instance.pk if self.instance else None

        if instance_pk: #the model is updated
            books_available = book.available(instance_pk)

        else: #the model is created
            books_available = book.available()

            if not customer.is_rent_available():
                self.add_error('customer', 'The customer can\'t rent')

        if amount_to_rent <= 0:
            self.add_error('amount_to_rent', 
                           'The amount to rent should be greater that 0')

        if amount_to_rent > books_available:
            self.add_error('amount_to_rent', 
                           'There are not enough books available')

        if rent_date > date.today():
            self.add_error('rent_date', 
                           'The rent date can\'t be in the future')

        if due_date < date.today():
            self.add_error('due_date', 'The due date can\'t be in the past')
        
        return data