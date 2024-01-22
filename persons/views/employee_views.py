from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from persons.models import Employee
from persons.forms.employee_forms import EmployeeForm
from libraries.forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'employee/employee_index.html'
    context_object_name = 'model_list'
    paginate_by = 4

    def get_queryset(self):
        library_id = self.kwargs.get('library_id')

        if library_id:
            return Employee.objects.filter(library_id=library_id)
        else:
            return Employee.objects.all()
    
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