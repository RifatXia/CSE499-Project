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
    days_available = models.CharField(max_length=100, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    class Meta:
        verbose_name_plural = "Doctors"

    def save(self, *args, **kwargs):
        self.is_doctor = True
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        start_day = self.days_available.split('-')[0].strip()
        end_day = self.days_available.split('-')[1].strip()

        selected_days = days[days.index(start_day):days.index(end_day) + 1]

        # Create and save the Doctor instance first
        doctor = super(Doctor, self).save(*args, **kwargs)

        # Create and save the Schedule associated with the Doctor
        schedule = Schedule.objects.create(
            doctor=doctor,
            start_time=self.start_time,
            end_time=self.end_time,
            days=", ".join(selected_days),
        )

# models for setting appointment and fetching the appointment dates
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    
    days = MultiSelectField(max_length=500, choices=DAYS)
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
