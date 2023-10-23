from django import forms
from .models import Person
from .models import Patient


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email','password']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'age', 'gen', 'email', 'phn', 'password']
        
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age