from django.db import models

from datetime import date

from libraries.services import RentService

class Rent(models.Model):
    book = models.ForeignKey('libraries.Book', on_delete = models.PROTECT)
    amount_to_rent = models.IntegerField(default = 1)
    customer = models.ForeignKey('persons.Customer', 
                                 on_delete = models.PROTECT, 
                                 related_name = 'rents_due')
    employee = models.ForeignKey('persons.Employee', 
                                 on_delete = models.PROTECT, 
                                 related_name = 'rents_done')
    library = models.ForeignKey('libraries.Library', 
                                on_delete = models.PROTECT, 
                                related_name = 'rents')
    created_date = models.DateField()
    modified_date = models.DateField()
    rent_date = models.DateField()
    due_date = models.DateField()
    status = models.ForeignKey('libraries.RentStatus', 
                               on_delete = models.PROTECT)

    def __str__(self):
        return f'{self.customer} - due date: {self.due_date}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_date = date.today()
            self.modified_date = date.today()
        else:
            self.modified_date = date.today()
        super().save(*args, **kwargs)

    def update_status(self):
        return RentService.update_status(self)