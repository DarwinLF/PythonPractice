from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Library
from ..forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'library/library_index.html'
    context_object_name = 'library_list'

    def get_queryset(self):
        #Person.objects.filter(age__gte = 18) orm
        #sum([x.age for x in listPerson if x.age >= 18])
        return Library.objects.all()
    
class AddView(generic.CreateView):
    model = Library
    form_class = LibraryForm
    template_name_suffix = '_create_form'
    template_name = 'library/library_create_form.html'
    success_url = reverse_lazy('libraries:library_index')

def LibraryCreate(request):
    form = LibraryForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return HttpResponseRedirect(reverse('libraries:library_index'))
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(request, 'library/library_create_form.html', {'form': form})

    else:
        return render(request, 'library/library_create_form.html', {'form': form})