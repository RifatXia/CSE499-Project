from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from .forms import PersonForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PersonSerializer
from django.http import JsonResponse
from .models import Doctor

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_person')
    else:
        form = PersonForm()

    return render(request, 'hospital/add_person.html', {'form': form})


def success(request):
    return render(request, 'hospital/success.html')

def login(request):
    return render(request, 'hospital/login.html')

from django.shortcuts import render
from .models import Person

# the method to fetch the user data and to edit it for both the android and the web
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_person(request, user_id):
    person = get_object_or_404(Person, id=user_id)

    # Check if the client wants JSON response (Android) or HTML response (Web)
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        if request.method == 'GET':
            serializer = PersonSerializer(person)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = PersonSerializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Return HTML template for web clients
        if request.method == 'GET':
            return render(request, 'hospital/person_details.html', {'person_data': person})
        
        elif request.method == 'POST':
            # Update data based on the form data from the web client
            person.name = request.data.get('name', person.name)
            person.dob = request.data.get('dob', person.dob)
            person.age = request.data.get('age', person.age)
            person.gen = request.data.get('gen', person.gen)
            person.email = request.data.get('email', person.email)
            person.phn = request.data.get('phn', person.phn)
            person.save()

            # Return a success response
            return redirect('success')
        
def doctor_list(request):
    doctors = Doctor.objects.all()
    # return render(request, 'doctors_info.html', {'doctors': doctors})
    return render(request, 'hospital/doctors_info.html', {'doctors': doctors})

def get_doctor(request,specialization):
    doctors = Doctor.objects.filter(specialization=specialization)
    # return render(request, 'doctors_info.html', {'doctors': doctors})
    return render(request, 'hospital/doctors_info.html', {'doctors': doctors})

def about(request):
    return render(request, 'hospital/about.html')

