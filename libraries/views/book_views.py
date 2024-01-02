from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Book
from ..forms.book_forms import BookForm

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

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('isbn', 'ISBN already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('libraries:book_index'))
    
class UpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_update.html'
    success_url = reverse_lazy('libraries:book_index')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('isbn', 'ISBN already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('libraries:book_index'))
    
class DetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'model'