from django.db import models
from .person import Person

from persons.services import CustomerService
    
class Customer(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT,
                                related_name='customers')
    credit_time = models.IntegerField(default = 7)
    status = models.ForeignKey('persons.CustomerStatus', 
                               on_delete = models.PROTECT)
    
    def IsRentAvailable(self):
        return CustomerService.IsRentAvailable(self.pk)
    
    def CheckRentAvailability(self):
        return CustomerService.CheckRentAvailability(self)