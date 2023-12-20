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
    
    def getAge(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    published_date = models.DateField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title