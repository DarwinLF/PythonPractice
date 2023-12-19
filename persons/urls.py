from django.urls import path

from . import views

app_name = 'persons'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddView.as_view(), name='add'),
    path('<int:pk>/', views.EditView.as_view(), name='edit'),
    path('create/', views.CreatePerson, name="createPerson"),
    path('<int:pk>/delete', views.DeleteView.as_view(), name="deletePerson")
]
