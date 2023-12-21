from django.contrib import admin

from .models import Library, Book, BookStatus, Rent

# Register your models here.

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(BookStatus)
admin.site.register(Rent)