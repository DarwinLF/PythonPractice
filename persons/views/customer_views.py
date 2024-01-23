from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from persons.models import Customer
from persons.forms.customer_forms import CustomerForm
from libraries.forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'customer/customer_index.html'
    context_object_name = 'model_list'
    paginate_by = 4

    def get_queryset(self):
        library_id = self.kwargs.get('library_id')

        if library_id:
            return Customer.objects.filter(library_id=library_id)
        else:
            return Customer.objects.all()
        
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
        modified_instances = [instance.CheckRentAvailability() 
                              for instance in queryset]

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
    
def create_modal(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'status': 'success', 'message': 
                                 'Form submitted successfully'})
        else:
            errors_html = render(request, 'customer/customer_create_form.html', 
                                 {'form': form}).content.decode('utf-8')
            return JsonResponse({'status': 'error', 'message': 
                                 'Form submission failed', 'errors': 
                                 errors_html}, status=400)
    else:
        form = CustomerForm()
    
    return render(request, 'customer/customer_create_form.html', {'form': form})