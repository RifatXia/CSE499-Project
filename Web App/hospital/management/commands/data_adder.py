from django.core.management.base import BaseCommand
from hospital.models import Doctor

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Open and read the text file with the data
        with open('doctor_info.txt', 'r') as file:
            lines = file.readlines()

        # doctors = []
        for i in range(0, len(lines), 11):
            doctor = Doctor.objects.create(
            name=lines[i + 0],
            dob=lines[i + 1],
            age=lines[i + 2],
            gen=lines[i + 3],
            email=lines[i + 4],
            phn=lines[i + 5],
            password=lines[i + 6],
            degree=lines[i + 7],
            specialization=lines[i + 8],
            keyword=lines[i + 9],
            image='static/images/ai.jpg',  # Default image value
        )