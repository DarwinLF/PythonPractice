from django.urls import path

from .views import libraries_views, library_views, book_views, rent_views, ajax_views

app_name = 'libraries'
urlpatterns = [
     path('', libraries_views.LibrariesLinks, name='libraries_index'),
     path('library/', library_views.IndexView.as_view(), name='library_index'),
     path('library/createLibrary/', library_views.CreateView.as_view(), 
          name='library_create'),
     path('library/<int:pk>/', library_views.DetailView.as_view(), 
          name='library_detail'),
     path('library/<int:pk>/updateLibrary', library_views.UpdateView.as_view(), 
          name='library_update'),
     path('book/', book_views.IndexView.as_view(), name='book_index'),
     path('book/createBook/', book_views.CreateView.as_view(), 
          name='book_create'),
     path('book/<int:pk>/', book_views.DetailView.as_view(), 
          name='book_detail'),
     path('book/<int:pk>/updateBook', book_views.UpdateView.as_view(), 
          name='book_update'),
     path('rent/', rent_views.IndexView.as_view(), name='rent_index'),
     path('rent/createRent/', rent_views.CreateView.as_view(), 
          name='rent_create'),
     path('rent/<int:pk>/', rent_views.DetailView.as_view(), 
          name='rent_detail'),
     path('rent/<int:pk>/updateRent', rent_views.UpdateView.as_view(), 
          name='rent_update'),
     path('rent/ajax/getLibrary/<int:pk>', ajax_views.RentAjaxView.as_view(),
          name='rent_ajax_library'),
     path('book/ajax/getAvailable/<int:pk>', 
          ajax_views.BookAvailableAjaxView.as_view(),
          name='book_ajax_available'),
     path('book/ajax/getAvailable/<int:book_pk>/<int:rent_pk>', 
     ajax_views.BookAvailableInUpdateAjaxView.as_view(),
     name='book_ajax_available_update'),
]
