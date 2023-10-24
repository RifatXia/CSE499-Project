from django import forms
from .models import Person
from .models import Patient

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age
