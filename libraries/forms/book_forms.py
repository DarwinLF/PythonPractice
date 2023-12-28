from django import forms
from django.utils import timezone

from ..models import Book
from mysite.function import validateIsbn13

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'published_date', 'isbn', 'quantity',
                   'rent_price', 'sale_price', 'author', 'status']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
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