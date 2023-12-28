from django.urls import path

from .views import library_views, libraries_views

app_name = 'libraries'
urlpatterns = [
    path('', libraries_views.LibrariesLinks, name='libraries_index'),
    path('library/', library_views.IndexView.as_view(), name='library_index'),
    path('library/createLibrary/', library_views.CreateView.as_view(), name='library_create'),
    path('library/<int:pk>/', library_views.UpdateView.as_view(), name='library_update'),
]
