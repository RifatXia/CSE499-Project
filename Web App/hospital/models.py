# from django.contrib.auth.models import User
# from django.db import models

# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     dob = models.DateField()
#     age = models.IntegerField()
#     gen = models.CharField(max_length=6)
#     email = models.EmailField()
#     phn = models.IntegerField()
#     password = models.CharField(max_length=100, default='123')

#     def __str__(self):
#         return self.name
    
# class Patient(Person):
#     address = models.CharField(max_length=200, default='Dhaka')

# class Doctor(Person):
#     image = models.ImageField(default='static/images/ai.jpg',upload_to='static/images/doctor_images')
#     degree = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     keyword = models.CharField(max_length=100)

# class Appointment(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     scheduled_time = models.DateTimeField()

#     def __str__(self):
#         return self.patient.name + " with " + self.doctor.name

# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     date_of_birth = models.DateField()
#     gender = models.CharField(max_length=10)

#     def __str__(self):
#         return self.user.username

# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     phn = models.IntegerField()
    
#     def save(self, *args, **kwargs):
#         # Create or update the User and UserProfile instances
#         user, created = User.objects.get_or_create(username=self.name, email=self.email, password=self.password)
#         user.first_name = self.name
#         user.save()
        
#         user_profile, created = UserProfile.objects.get_or_create(user=user)
#         user_profile.date_of_birth = self.dob
#         user_profile.gender = self.gen
#         user_profile.save()

#         super(Person, self).save(*args, **kwargs)

# class Patient(User, UserProfile):
#     address = models.CharField(max_length=200, default='Dhaka')

# class Doctor(User, UserProfile):
#     image = models.ImageField(default='static/images/ai.jpg', upload_to='static/images/doctor_images')
#     degree = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     keyword = models.CharField(max_length=100)

# class Appointment(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     scheduled_time = models.DateTimeField()

#     def __str__(self):
#         return f"{self.patient.name} with {self.doctor.name}"

from django.contrib.auth.models import User
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    gen = models.CharField(max_length=6)
    email = models.EmailField()
    phn = models.IntegerField()
    password = models.CharField(max_length=100, default='123')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        user, created = User.objects.get_or_create(username=self.email, email=self.email)
        if created:
            user.set_password(self.password)
            user.save()

        super(Person, self).save(*args, **kwargs)


class Patient(Person):
    address = models.CharField(max_length=200, default='Dhaka')

class Doctor(Person):
    image = models.ImageField(default='static/images/ai.jpg', upload_to='static/images/doctor_images')
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)

class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name}"
