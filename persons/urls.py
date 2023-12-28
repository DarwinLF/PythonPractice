from django.urls import path

from .views import author_views, person_views

app_name = 'persons'
urlpatterns = [
    path('', person_views.PersonLinks, name='person_index'),
    path('author/', author_views.IndexView.as_view(), name='author_index'),
    path('author/createAuthor/', author_views.CreateView.as_view(), name='author_create'),
    path('author/<int:pk>/', author_views.DetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/updateAuthor', author_views.UpdateView.as_view(), name='author_update'),
    # path('addPerson/', views.PersonAddView.as_view(), name='person_add'),
    # path('createPerson/', views.createPerson, name="person_create"),
    # path('<int:pk>/', views.PersonEditView.as_view(), name='person_edit'),
    # path('<int:pk>/deletePerson', views.PersonDeleteView.as_view(), name="person_delete")
]
