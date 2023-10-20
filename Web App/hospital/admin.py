from django.contrib import admin
from .models import Person, Doctor

admin.site.register(Person)
admin.site.register(Doctor)