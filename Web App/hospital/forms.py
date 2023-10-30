from django import forms
from .models import Person, Patient, Appointment, Doctor

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email', 'password']


class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    gen = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'age', 'gen', 'email', 'password', 'phn']

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.TextInput(),  # Leave the widget for address as default
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age
    
class DoctorForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    gen = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    class Meta:
        model = Doctor
        exclude = ['is_doctor']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age
    
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
