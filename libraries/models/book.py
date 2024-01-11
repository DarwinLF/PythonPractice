from django.db import models

from libraries.services import BookService

class Book(models.Model):
    title = models.CharField(max_length = 200)
    published_date = models.DateField()
    isbn = models.CharField(max_length = 17, unique = True )
    quantity = models.IntegerField(default = 0)
    rent_price = models.FloatField(default = 0.0)
    sale_price = models.FloatField(default = 0.0)
    author = models.ForeignKey('persons.Author', 
                               on_delete = models.PROTECT, 
                               related_name = 'books')
    status = models.ForeignKey('libraries.BookStatus', 
                               on_delete = models.PROTECT)
    library = models.ForeignKey('libraries.Library', 
                                on_delete = models.PROTECT,
                                related_name = 'books')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.isbn = self.isbn.replace('-', '')
        super().save(*args, **kwargs)

    def rented(self, rent_pk):
        if rent_pk == 0:
            return self.library.rents.aggregate(
                total_rented=models.Sum('amount_to_rent'))['total_rented'] \
                    or 0
        else:
            return self.library.rents.exclude(pk=rent_pk).aggregate(
                total_rented=models.Sum('amount_to_rent'))['total_rented'] \
                    or 0
    
    def available(self, rent_pk=0):
        return self.quantity - self.rented(rent_pk)
    
    def AdjustStatusOfBook(self):
        return BookService.AdjustStatusOfBook(self.pk)