from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from libraries.models import Rent
from libraries.forms.rent_forms import RentForm
from libraries.forms.library_forms import LibraryForm
from libraries.forms.book_forms import BookForm
from persons.forms.customer_forms import CustomerForm
from persons.forms.employee_forms import EmployeeForm

class IndexView(generic.ListView):
    template_name = 'rent/rent_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Rent.objects.all()
    
class CreateView(generic.CreateView):
    model = Rent
    form_class = RentForm
    template_name_suffix = '_create_form'
    template_name = 'rent/rent_create_form.html'
    success_url = reverse_lazy('libraries:rent_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        context['book_form'] = BookForm()
        context['customer_form'] = CustomerForm()
        context['employee_form'] = EmployeeForm()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)

        #import ipdb; ipdb.set_trace()

        #AdjustStatusOfBook(form.instance.book.pk)
        form.instance.book.AdjustStatusOfBook()

        return response
    
class UpdateView(generic.UpdateView):
    model = Rent
    form_class = RentForm
    template_name = 'rent/rent_update.html'
    success_url = reverse_lazy('libraries:rent_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rent = self.object
        context['selected_book'] = rent.book.pk
        context['selected_customer'] = rent.customer.pk
        context['selected_employee'] = rent.employee.pk

        context['library_form'] = LibraryForm()
        context['book_form'] = BookForm()
        context['customer_form'] = CustomerForm()
        context['employee_form'] = EmployeeForm()

        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)

        form.instance.book.AdjustStatusOfBook()

        #import ipdb; ipdb.set_trace()

        return response
    
class DetailView(generic.DetailView):
    model = Rent
    template_name = 'rent/rent_detail.html'
    context_object_name = 'model'