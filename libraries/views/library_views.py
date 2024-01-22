from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Library
from ..forms.library_forms import LibraryForm

class IndexView(generic.ListView):
    template_name = 'library/library_index.html'
    context_object_name = 'model_list'
    paginate_by = 4

    def get_queryset(self):
        return Library.objects.all()
    
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
    model = Library
    form_class = LibraryForm
    template_name_suffix = '_create_form'
    template_name = 'library/library_create_form.html'
    success_url = reverse_lazy('libraries:library_index')
    
class UpdateView(generic.UpdateView):
    model = Library
    form_class = LibraryForm
    template_name = 'library/library_update.html'
    success_url = reverse_lazy('libraries:library_index')
    
class DetailView(generic.DetailView):
    model = Library
    template_name = 'library/library_detail.html'
    context_object_name = 'model'