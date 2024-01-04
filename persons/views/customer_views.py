from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Customer
from ..forms.customer_forms import CustomerForm

class IndexView(generic.ListView):
    template_name = 'customer/customer_index.html'
    context_object_name = 'model_list'

    def get_queryset(self):
        return Customer.objects.all()
    
class CreateView(generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name_suffix = '_create_form'
    template_name = 'customer/customer_create_form.html'
    success_url = reverse_lazy('persons:customer_index')

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