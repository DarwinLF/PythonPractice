from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from .models import Person
from .forms import PersonForm

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'persons/index.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        #Person.objects.filter(age__gte = 18) orm
        #sum([x.age for x in listPerson if x.age >= 18])
        return Person.objects.all()
    
    
    
class AddView(generic.CreateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_create_form'
    template_name = 'persons/person_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        persons = self.model.objects.all()
        if persons.exists():
            context["person"] = persons.last()
            
        return context
    
    
class EditView(generic.UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'persons/edit.html'
    success_url = reverse_lazy('persons:index')

class DeleteView(generic.DeleteView):
    model = Person
    template_name = 'persons/confirm_delete.html'
    success_url = reverse_lazy('persons:index')
    
def CreatePerson(request):
    form = PersonForm(request.POST)
    if form.is_valid():
        try:
            new_person = form.save()
            return HttpResponseRedirect(reverse('persons:index'))
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(request, 'persons/person_create_form.html', {'form': form})

    else:
        return render(request, 'persons/person_create_form.html', {'form': form})
            
    