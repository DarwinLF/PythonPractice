from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Employee
from ..forms.employee_forms import EmployeeForm

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

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('persons:employee_index'))
    
class UpdateView(generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_update.html'
    success_url = reverse_lazy('persons:employee_index')

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except IntegrityError as e:
            form.add_error('rnc', 'RNC already exists')
            return render(self.request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('persons:employee_index'))
    
class DetailView(generic.DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'