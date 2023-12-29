from django.urls import path

from .views import libraries_views, library_views, book_views, rent_views

app_name = 'libraries'
urlpatterns = [
    path('', libraries_views.LibrariesLinks, name='libraries_index'),
    path('library/', library_views.IndexView.as_view(), name='library_index'),
    path('library/createLibrary/', library_views.CreateView.as_view(), name='library_create'),
    path('library/<int:pk>/', library_views.DetailView.as_view(), name='library_detail'),
    path('library/<int:pk>/updateLibrary', library_views.UpdateView.as_view(), name='library_update'),
    path('book/', book_views.IndexView.as_view(), name='book_index'),
    path('book/createBook/', book_views.CreateView.as_view(), name='book_create'),
    path('book/<int:pk>/', book_views.DetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/updateBook', book_views.UpdateView.as_view(), name='book_update'),
    path('rent/', rent_views.IndexView.as_view(), name='rent_index'),
    path('rent/createRent/', rent_views.CreateView.as_view(), name='rent_create'),
    path('rent/<int:pk>/', rent_views.DetailView.as_view(), name='rent_detail'),
    path('rent/<int:pk>/updateRent', rent_views.UpdateView.as_view(), name='rent_update'),
]
