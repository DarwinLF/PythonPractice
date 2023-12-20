from django.urls import path

from . import views

app_name = 'persons'
urlpatterns = [
    path('', views.PersonIndexView.as_view(), name='person_index'),
    path('addPerson/', views.PersonAddView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonEditView.as_view(), name='person_edit'),
    path('createPerson/', views.createPerson, name="person_create"),
    path('<int:pk>/deletePerson', views.PersonDeleteView.as_view(), name="person_delete")
]
