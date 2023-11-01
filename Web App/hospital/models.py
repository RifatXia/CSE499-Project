from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta, date
from multiselectfield import MultiSelectField

class Person(User):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    gen = models.CharField(max_length=6)
    phn = models.IntegerField()
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.username = self.email
        self.set_password(self.password) 
        super(Person, self).save(*args, **kwargs)

class Patient(Person):
    address = models.CharField(max_length=200, default='Dhaka')
    
    class Meta:
        verbose_name_plural = "Patients"

class Doctor(Person):
    image = models.ImageField(default='static/images/ai.jpg', upload_to='static/images/doctor_images')
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Doctors"

    def save(self, *args, **kwargs):
        self.is_doctor = True
        super(Doctor, self).save(*args, **kwargs)

# models for setting appointment and fetching the appointment dates
class Schedule(models.Model):
    DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = MultiSelectField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.doctor.name

class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name}"
