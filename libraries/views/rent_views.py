from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError

from ..models import Rent
from ..forms.rent_forms import RentForm

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
    
class UpdateView(generic.UpdateView):
    model = Rent
    form_class = RentForm
    template_name = 'rent/rent_update.html'
    success_url = reverse_lazy('libraries:rent_index')
    
class DetailView(generic.DetailView):
    model = Rent
    template_name = 'rent/rent_detail.html'
    context_object_name = 'model'