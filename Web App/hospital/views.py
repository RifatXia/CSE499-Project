from django.shortcuts import render, redirect
from .forms import PersonForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PersonSerializer
from django.http import JsonResponse

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

# @api_view(['GET'])
# def get_person(request, user_id):
#     try:
#         person = Person.objects.get(pk=user_id)
#         serializer = PersonSerializer(person)
#         return Response(serializer.data)
#     except Person.DoesNotExist:
#         return Response(status=404)

def get_person(request, user_id):
    try:
        person = Person.objects.get(id=user_id)
    except Person.DoesNotExist:
        person = None

    if person:
        serializer = PersonSerializer(person)

        if request.META.get('HTTP_ACCEPT') == 'application/json':
            # If the request accepts JSON response (e.g., Android app)
            return JsonResponse(serializer.data)
        else:
            # If the request is from a web browser, render the HTML template
            return render(request, 'hospital/person_details.html', {'person_data': serializer.data})
    else:
        return JsonResponse({'error': 'Person not found'}, status=404)


