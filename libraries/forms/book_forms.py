from django import forms
from django.utils import timezone

from ..models import Book
from mysite.function import validateIsbn13

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'published_date', 'isbn', 'quantity',
                   'rent_price', 'sale_price', 'author', 'library', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'library': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = self.cleaned_data
        isbn = data['isbn']
        pub_date = data['published_date']

        if not validateIsbn13(isbn):
            self.add_error('isbn', 'Invalid ISBN')

        if pub_date > timezone.now().date():
            self.add_error('published_date', 'The published date can\'t be in the future')
        
        return data