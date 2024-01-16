from django.contrib import admin

from .models import Library, Book, BookStatus, BookGenders, Rent, RentStatus

# Register your models here.

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(BookStatus)
admin.site.register(BookGenders)
admin.site.register(Rent)
admin.site.register(RentStatus)