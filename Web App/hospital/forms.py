from base64 import urlsafe_b64encode
from django import forms
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes
from .models import Person, Patient, Appointment, Doctor
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils.translation import gettext as _

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gen': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phn': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),  # Leave the widget for address as default
        }

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}))

    def clean_password(self):
        password = self.cleaned_data['password']

        # Custom password validation
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters."),
                code='password_too_short',
            )

        if password.isdigit():
            raise ValidationError(
                _("Password can't be entirely numeric."),
                code='password_entirely_numeric',
            )

        return password
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    gen = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'age', 'gen', 'email', 'password', 'phn', 'address']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gen': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phn': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),  # Leave the widget for address as default
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

    gen = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Doctor
        exclude = ['is_doctor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gen': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phn': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise forms.ValidationError("Age cannot be negative.")
        return age
    
<<<<<<< HEAD
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['scheduled_time']
        widgets = {           
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
=======
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['scheduled_time']
#         widgets = {
#             'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }
>>>>>>> 6678660279afe38d1df66a98cfa1d7a1fb4b2aab

# password reset form 
class CustomPasswordResetForm(PasswordResetForm):
    # Define your custom subject and email template names
    subject_template_name = 'password/custom_password_reset_subject.txt'
    email_template_name = 'password/custom_password_reset_email.html'

    def save(self, request=None, **kwargs):
        email = self.cleaned_data['email']
        person = Person.objects.get(email=email)

        # Construct reset URL (similar to the view)
        uid = urlsafe_base64_encode(force_bytes(person.pk))
        token = default_token_generator.make_token(person)
        token_url = reverse('custom_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_url = self.request.build_absolute_uri(token_url)

        # Pass reset_url as context to the email template
        context = {'reset_url': reset_url}

        # Send the email using the provided email template
        self.send_mail(
            request, self.subject_template_name, self.email_template_name,
            context, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
        )
