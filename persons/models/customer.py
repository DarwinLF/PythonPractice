from django.db import models
from .person import Person

from persons.services import CustomerService
    
class Customer(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT,
                                related_name='customers')
    credit_time = models.IntegerField(default = 7)
    status = models.ForeignKey('persons.CustomerStatus', 
                               on_delete = models.PROTECT)
    
    def is_rent_available(self):
        return CustomerService.is_rent_available(self.pk)
    
    def update_status(self):
        return CustomerService.update_status(self)