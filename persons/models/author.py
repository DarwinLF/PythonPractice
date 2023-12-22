from django.db import models
from .person import Person

class Author(Person):
    alias = models.CharField(max_length=100)
    
    def __str__(self):
        return super().__str__() + f" ({self.alias})"