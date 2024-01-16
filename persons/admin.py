from django.contrib import admin

from .models import Author, Customer, CustomerStatus, Employee

# Register your models here.
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(CustomerStatus)
admin.site.register(Employee)