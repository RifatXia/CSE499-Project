from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PersonSerializer
from django.http import JsonResponse
from .models import Doctor, Patient
from .forms import PatientForm, PersonForm, AppointmentForm
from .models import Doctor, Patient, Appointment
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

# patient signup 
def add_person(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            person = Patient.objects.filter(email=email, password=password).first()

            if person == None:
                form.save()
            return redirect('get_homepage')
    else:
        form = PatientForm()

    return render(request, 'hospital/add_person.html', {'form': form})

def success(request):
    return render(request, 'hospital/success.html')
        
def doctor_list(request):
    doctors = Doctor.objects.all()
    # return render(request, 'doctors_info.html', {'doctors': doctors})
    return render(request, 'hospital/doctors_info.html', {'doctors': doctors})

def get_doctor(request,keyword):
    doctors = Doctor.objects.filter(keyword=keyword)
    return render(request, 'hospital/doctors_info.html', {'doctors': doctors})

def about(request):
    return render(request, 'hospital/about.html')

def contact(request):
    return render(request, 'hospital/contact.html')

def send_email(patient,doctor,appointment):
    subject = 'Confirmation of Appointment'
    message = f'Hi {patient.name}, Your appointment is confirmed for Dr. {doctor.name} {appointment.scheduled_time}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [patient.email, ]
    send_mail( subject, message, email_from, recipient_list )

# make appointment with a doctor
@login_required 
def make_appointment(request, doctor_id):
    patient_id = request.user.id - len(Doctor.objects.all()) - 2
    patient = Patient.objects.get(id=patient_id)
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            scheduled_time = form.cleaned_data['scheduled_time']
            # Create the appointment
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.scheduled_time = scheduled_time
            appointment.save()
            send_email(patient,doctor,appointment)
            

            return redirect('get_homepage')
    else:
        form = AppointmentForm()

    return render(request, 'hospital/appointment.html', {'person' : patient, 'doctor' : doctor, 'form': form})

# successful login of the user 
def login_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('get_homepage')
        else:
            return HttpResponse('Invalid email or password. Please try again.')
    else:
        form = PersonForm()

    return render(request, 'hospital/login.html', {'form': form})

# fetching the user information 
@login_required
def get_person(request):
    person_id = request.user.id - len(Doctor.objects.all()) - 2
    print(person_id)
    patient = Patient.objects.get(id=person_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        print(form)
        if form.is_valid():
            form.save()
            print('Profile updated successfully')
            return redirect('get_homepage')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/person_details.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('get_homepage')
