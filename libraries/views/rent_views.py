from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from libraries.models import Rent
from libraries.forms.rent_forms import RentForm
from libraries.forms.library_forms import LibraryForm
from libraries.forms.book_forms import BookForm
from persons.forms.customer_forms import CustomerForm
from persons.forms.employee_forms import EmployeeForm

class IndexView(generic.ListView):
    model = Rent
    template_name = 'rent/rent_index.html'
    context_object_name = 'model_list'
    paginate_by = 4

    def get_queryset(self):
        return Rent.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            model_list = paginator.page(page)
        except PageNotAnInteger:
            model_list = paginator.page(1)
        except EmptyPage:
            model_list = paginator.page(paginator.num_pages)

        context[self.context_object_name] = model_list

        return context
    
    def get(self, request, *args, **kwargs):
        # Get the original queryset
        queryset = self.get_queryset()

        # Modify each instance using your_model_method
        modified_instances = [rent.update_status() 
                              for rent in queryset]
        
        if modified_instances[0]:
            modified_instances[0].customer = modified_instances[0].customer.update_status()

        # Override the object_list attribute with the modified instances
        self.object_list = modified_instances

        return super().get(request, *args, **kwargs)
    
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
        form.instance.book.adjust_status()
        form.instance.customer.update_status()

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

        form.instance.book.adjust_status()
        form.instance.customer.update_status()

        #import ipdb; ipdb.set_trace()

        return response
    
    def get(self, request, *args, **kwargs):
        # Get the Rent object
        rent = self.get_object()

        # Run update_status before rendering the page
        rent = rent.update_status()
        rent.customer = rent.customer.update_status()

        return super().get(request, *args, **kwargs)
    
class DetailView(generic.DetailView):
    model = Rent
    template_name = 'rent/rent_detail.html'
    context_object_name = 'model'

    def get_object(self, queryset=None):
        rent = super().get_object(queryset=queryset)
        #import ipdb; ipdb.set_trace()
        rent = rent.update_status()
        rent.customer = rent.customer.update_status()
        return rent