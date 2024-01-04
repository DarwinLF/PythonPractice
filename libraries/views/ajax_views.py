from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize

from libraries.models import Library

class RentAjaxView(View):
    def get(self, request, *args, **kwargs):
        libraryId = self.kwargs.get('pk')

        library = get_object_or_404(Library, pk=libraryId)

        books = serialize('json', library.books.all())
        customers = serialize('json', library.customers.all())
        employees = serialize('json', library.employees.all())

        return JsonResponse({'customers': customers, 'books': books, 'employees': employees})