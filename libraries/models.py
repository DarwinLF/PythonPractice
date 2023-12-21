from django.db import models

# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 200)

    def __str__(self):
        return self.name
    
class BookStatus(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length = 200)
    published_date = models.DateField()
    isbn = models.CharField(max_length = 13, unique = True )
    quantity = models.IntegerField(default = 0)
    rent_price = models.FloatField(default = 0.0)
    sale_price = models.FloatField(default = 0.0)
    author = models.ForeignKey('persons.Author', on_delete = models.PROTECT, related_name = 'books')
    status = models.ForeignKey(BookStatus, on_delete = models.PROTECT)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.isbn = self.isbn.replace('-', '')
        super().save(*args, **kwargs)

class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete = models.PROTECT)
    customer = models.ForeignKey('persons.Customer', on_delete = models.PROTECT, related_name = 'rents_due')
    employee = models.ForeignKey('persons.Employee', on_delete = models.PROTECT, related_name = 'rents_done')
    library = models.ForeignKey(Library, on_delete = models.PROTECT, related_name = 'rents')
    rent_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f'{self.customer} - due date: {self.due_date}'
