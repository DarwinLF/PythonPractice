from django.db import models
from .person import Person
    
class Customer(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT, related_name='customers')