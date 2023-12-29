from django.db import models

from datetime import date

class Rent(models.Model):
    book = models.ForeignKey('libraries.Book', on_delete = models.PROTECT)
    customer = models.ForeignKey('persons.Customer', 
                                 on_delete = models.PROTECT, 
                                 related_name = 'rents_due')
    employee = models.ForeignKey('persons.Employee', 
                                 on_delete = models.PROTECT, 
                                 related_name = 'rents_done')
    library = models.ForeignKey('libraries.Library', 
                                on_delete = models.PROTECT, 
                                related_name = 'rents')
    rent_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f'{self.customer} - due date: {self.due_date}'
    
    def save(self, *args, **kwargs):
        self.rent_date = date.today()
        super().save(*args, **kwargs)