from django.urls import path

from .views import library_views

app_name = 'libraries'
urlpatterns = [
    path('', library_views.IndexView.as_view(), name='library_index'),
    path('createLibrary/', library_views.AddView.as_view(), name='library_create'),
    path('<int:pk>/', library_views.EditView.as_view(), name='library_edit'),
]
