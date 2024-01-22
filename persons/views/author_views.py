from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Author
from ..forms.author_forms import AuthorForm

class IndexView(generic.ListView):
    template_name = 'author/author_index.html'
    context_object_name = 'model_list'
    paginate_by = 4

    def get_queryset(self):
        return Author.objects.all()
    
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
    model = Author
    form_class = AuthorForm
    template_name_suffix = '_create_form'
    template_name = 'author/author_create_form.html'
    success_url = reverse_lazy('persons:author_index')

#   def get_context_data(self, **kwargs):
#         context = super(PersonAddView, self).get_context_data(**kwargs)
#         persons = self.model.objects.all()
#         if persons.exists():
#             context["person"] = persons.last()
    
class UpdateView(generic.UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author/author_update.html'
    success_url = reverse_lazy('persons:author_index')
    
class DetailView(generic.DetailView):
    model = Author
    template_name = 'author/author_detail.html'
    context_object_name = 'model'