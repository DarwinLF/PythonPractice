from django.db import models

class Library(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 200)
    rnc = models.CharField(max_length = 13, 
                           unique = True,)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.rnc = self.rnc.replace('-', '')
        super().save(*args, **kwargs)