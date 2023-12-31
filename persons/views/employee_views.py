from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from persons.models import Employee
from persons.forms.employee_forms import EmployeeForm
from libraries.forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'employee/employee_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Employee.objects.all()
    
class CreateView(generic.CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name_suffix = '_create_form'
    template_name = 'employee/employee_create_form.html'
    success_url = reverse_lazy('persons:employee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        return context
    
class UpdateView(generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_update.html'
    success_url = reverse_lazy('persons:employee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        return context
    
class DetailView(generic.DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'model'