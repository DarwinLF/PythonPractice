from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize

from libraries.models import Library, Book

class RentAjaxView(View):
    def get(self, request, *args, **kwargs):
        libraryId = self.kwargs.get('pk')

        library = get_object_or_404(Library, pk=libraryId)

        books = serialize('json', library.books.all())
        customers = serialize('json', library.customers.all())
        employees = serialize('json', library.employees.all())

        return JsonResponse({'customers': customers, 'books': books, 'employees': employees})
    
class BookAvailableAjaxView(View):
    def get(self, request, *args, **kwargs):
        bookId = self.kwargs.get('pk')

        book = get_object_or_404(Book, pk=bookId)

        return JsonResponse({'availableBooks': book.available})