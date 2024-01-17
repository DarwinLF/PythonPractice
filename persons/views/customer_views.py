from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from persons.models import Customer
from persons.forms.customer_forms import CustomerForm
from libraries.forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'customer/customer_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        library_id = self.kwargs.get('library_id')

        if library_id:
            return Customer.objects.filter(library_id=library_id)
        else:
            return Customer.objects.all()
        
    def get(self, request, *args, **kwargs):
        # Get the original queryset
        queryset = self.get_queryset()

        # Modify each instance using your_model_method
        modified_instances = [instance.CheckRentAvailability() for instance in queryset]

        # Override the object_list attribute with the modified instances
        self.object_list = modified_instances

        return super().get(request, *args, **kwargs)
    
class CreateView(generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name_suffix = '_create_form'
    template_name = 'customer/customer_create_form.html'
    success_url = reverse_lazy('persons:customer_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        return context

    # def form_valid(self, form):
    #     try:
    #         super().form_valid(form)
    #     except IntegrityError as e:
    #         form.add_error('rnc', 'RNC already exists')
    #         return render(self.request, self.template_name, {'form': form})

    #     return HttpResponseRedirect(reverse('persons:customer_index'))
    
class UpdateView(generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_update.html'
    success_url = reverse_lazy('persons:customer_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_form'] = LibraryForm()
        return context

    # def form_valid(self, form):
    #     try:
    #         super().form_valid(form)
    #     except IntegrityError as e:
    #         form.add_error('rnc', 'RNC already exists')
    #         return render(self.request, self.template_name, {'form': form})

    #     return HttpResponseRedirect(reverse('persons:customer_index'))
    
class DetailView(generic.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'model'

    def get_object(self, queryset=None):
        # Get the original object using the parent method
        obj = super().get_object(queryset=queryset)

        # Modify the object using your_model_method
        modified_object = obj.CheckRentAvailability()

        return modified_object