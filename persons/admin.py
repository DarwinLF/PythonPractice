from django.contrib import admin

from .models import Author, Customer, Employee

# Register your models here.
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Employee)