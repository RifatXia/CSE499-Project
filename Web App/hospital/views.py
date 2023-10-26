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
from .forms import PatientForm, PersonForm
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

# def login(request):
     
#      return render(request, 'hospital/login.html')

# the method to fetch the user data and to edit it for both the android and the web
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def get_person(request, user_id):
#     person = get_object_or_404(Patient, id=user_id)

#     # Return HTML template for web clients
#     if request.method == 'GET':
#         return render(request, 'hospital/person_details.html', {'person_data': person})
    
#     elif request.method == 'POST':
#         # Update data based on the form data from the web client
#         person.name = request.data.get('name', person.name)
#         person.dob = request.data.get('dob', person.dob)
#         person.age = request.data.get('age', person.age)
#         person.gen = request.data.get('gen', person.gen)
#         person.email = request.data.get('email', person.email)
#         person.phn = request.data.get('phn', person.phn)
#         person.password = request.data.get('password', person.password)
#         person.save()

#         # Return a success response
#         return redirect('success')
        
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

# make appointment with a doctor 
def make_appointment(request, patient_id, doctor_id):
    doctor = Doctor.objects.filter(id=doctor_id)
    patient = Patient.objects.filter(id=patient_id)

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

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


@login_required
def get_person(request):
    person = request.user
    user_id = person.id
    print(user_id)
    context = {'user id': user_id}
    return render(request, 'hospital/person_details.html', context, {'person_data': person})

def logout_view(request):
    auth_logout(request)
    return redirect('get_homepage') 

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import PersonForm, PatientForm

# def register_person(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('get_homepage')
#     else:
#         form = PatientForm()

#     return render(request, 'hospital/register_person.html', {'form': form})
