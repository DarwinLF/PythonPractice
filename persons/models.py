from django.db import models
from django.urls import reverse

from datetime import date

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    rnc = models.CharField(max_length=13, unique=True)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse("persons:person_index")
    
    def save(self, *args, **kwargs):
        self.rnc = self.rnc.replace('-', '')
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
    
    # def getAge(self):
    #     today = date.today()
    #     return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
class Customer(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT, related_name='customers')

class Author(Person):
    alias = models.CharField(max_length=100)
    def __str__(self):
        return super().__str__() + f" ({self.alias})"

class Employee(Person):
    library = models.ForeignKey('libraries.Library', on_delete=models.PROTECT, related_name='employees')