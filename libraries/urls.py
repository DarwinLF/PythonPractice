from django.urls import path

from .views import library_views

app_name = 'libraries'
urlpatterns = [
    path('', library_views.IndexView.as_view(), name='library_index'),
    path('addPerson/', library_views.AddView.as_view(), name='library_add'),
    path('createPerson/', library_views.LibraryCreate, name="library_create"),
]
