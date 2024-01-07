from django.db import models

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
    status = models.ForeignKey('libraries.BookStatus', on_delete = models.PROTECT)
    library = models.ForeignKey('libraries.Library', 
                                on_delete = models.PROTECT,
                                related_name = 'books')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.isbn = self.isbn.replace('-', '')
        super().save(*args, **kwargs)

    @property
    def rented(self):
        return self.library.rents.aggregate(total_rented=models.Sum('amount_to_rent'))['total_rented'] or 0
        #return sum([x.amount_to_rent for x in self.library.rents.all()])
    
    @property
    def available(self):
        return self.quantity - self.rented