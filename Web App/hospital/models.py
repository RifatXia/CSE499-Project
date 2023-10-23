from django.db import models
from datetime import date

class Person(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    gen = models.CharField(max_length=6)
    email = models.EmailField()
    phn = models.IntegerField()

    def __str__(self):
        return self.name
    
class Patient(Person):
    address = models.CharField(max_length=200, default='Dhaka')

class Doctor(Person):
    image = models.ImageField(default='static/images/ai.jpg',upload_to='static/images/doctor_images')
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)