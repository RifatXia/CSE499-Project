from django import forms
from .models import Person, Patient, Appointment

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email', 'password']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

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