from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Author
from ..forms.author_forms import AuthorForm

class IndexView(generic.ListView):
    template_name = 'author/author_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Author.objects.all()
    
class CreateView(generic.CreateView):
    model = Author
    form_class = AuthorForm
    template_name_suffix = '_create_form'
    template_name = 'author/author_create_form.html'
    success_url = reverse_lazy('persons:author_index')

#   def get_context_data(self, **kwargs):
#         context = super(PersonAddView, self).get_context_data(**kwargs)
#         persons = self.model.objects.all()
#         if persons.exists():
#             context["person"] = persons.last()
            
#         return context
    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('persons:author_index'))
    
class UpdateView(generic.UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author/author_update.html'
    success_url = reverse_lazy('persons:author_index')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('persons:author_index'))
    
class DetailView(generic.DetailView):
    model = Author
    template_name = 'author/author_detail.html'
    context_object_name = 'model'