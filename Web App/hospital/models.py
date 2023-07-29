from django.db import models
from datetime import date

class Person(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    gen = models.CharField(max_length=6)
    email = models.EmailField()
    phn = models.IntegerField()

