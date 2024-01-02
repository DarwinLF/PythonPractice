from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Library
from ..forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'library/library_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Library.objects.all()
    
class CreateView(generic.CreateView):
    model = Library
    form_class = LibraryForm
    template_name_suffix = '_create_form'
    template_name = 'library/library_create_form.html'
    success_url = reverse_lazy('libraries:library_index')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('libraries:library_index'))
    
class UpdateView(generic.UpdateView):
    model = Library
    form_class = LibraryForm
    template_name = 'library/library_update.html'
    success_url = reverse_lazy('libraries:library_index')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('libraries:library_index'))
    
class DetailView(generic.DetailView):
    model = Library
    template_name = 'library/library_detail.html'
    context_object_name = 'model'