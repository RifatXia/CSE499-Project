from django.db import models
from datetime import date

class Person(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField(default=date.today)
    age = models.IntegerField(default=1)
    gen = models.CharField(max_length=6,default='Male')
    email = models.EmailField(default='sky@gmail.com')
    phn = models.IntegerField(default=1)

