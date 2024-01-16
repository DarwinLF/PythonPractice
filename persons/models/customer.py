from django.db import models
from .person import Person
    
class Customer(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT, related_name='customers')
    credit_time = models.IntegerField(default = 0)
    status = models.ForeignKey('persons.CustomerStatus', 
                               on_delete = models.PROTECT)