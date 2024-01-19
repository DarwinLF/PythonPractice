from django.urls import path

from .views import person_views, author_views, customer_views, employee_views

app_name = 'persons'
urlpatterns = [
    path('', person_views.PersonLinks, name='person_index'),
    path('author/', author_views.IndexView.as_view(), name='author_index'),
    path('author/createAuthor/', author_views.CreateView.as_view(), name='author_create'),
    path('author/<int:pk>/', author_views.DetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/updateAuthor/', author_views.UpdateView.as_view(), name='author_update'),
    path('customer/', customer_views.IndexView.as_view(), name='customer_index'),
    path('customer/createCustomer/', customer_views.CreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/', customer_views.DetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/updateCustomer/', customer_views.UpdateView.as_view(), name='customer_update'),
    path('employee/', employee_views.IndexView.as_view(), name='employee_index'),
    path('employee/createEmployee/', employee_views.CreateView.as_view(), name='employee_create'),
    path('employee/<int:pk>/', employee_views.DetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/updateEmployee/', employee_views.UpdateView.as_view(), name='employee_update'),
]
