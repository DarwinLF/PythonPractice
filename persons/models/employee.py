from django.db import models
from .person import Person

class Employee(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT, related_name='employees')