from django.urls import path

from .views import libraries_views, library_views, book_views

app_name = 'libraries'
urlpatterns = [
    path('', libraries_views.LibrariesLinks, name='libraries_index'),
    path('library/', library_views.IndexView.as_view(), name='library_index'),
    path('library/createLibrary/', library_views.CreateView.as_view(), name='library_create'),
    path('library/<int:pk>/', library_views.UpdateView.as_view(), name='library_update'),
    path('book/', book_views.IndexView.as_view(), name='book_index'),
    path('book/createBook/', book_views.CreateView.as_view(), name='book_create'),
    path('book/<int:pk>/', book_views.UpdateView.as_view(), name='book_update'),
]
