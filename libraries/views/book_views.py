from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from libraries.models import Book
from libraries.forms.book_forms import BookForm
from libraries.forms.library_forms import LibraryForm
from persons.forms.author_forms import AuthorForm

class IndexView(generic.ListView):
    template_name = 'book/book_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Book.objects.all()
    
class CreateView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name_suffix = '_create_form'
    template_name = 'book/book_create_form.html'
    success_url = reverse_lazy('libraries:book_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        context['author_form'] = AuthorForm()
        return context
    
class UpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_update.html'
    success_url = reverse_lazy('libraries:book_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        context['author_form'] = AuthorForm()
        return context
    
class DetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'model'