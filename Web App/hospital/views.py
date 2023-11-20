from base64 import urlsafe_b64encode
from django.shortcuts import render, redirect
from .models import Person, Doctor, Patient, Appointment, Schedule
from .forms import PatientForm, PersonForm, AppointmentForm, DoctorForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from .forms import CustomPasswordResetForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import json

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

def validate_custom_password(password):
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

def success(request):
    return render(request, 'hospital/success.html')
        
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

def send_email(patient,doctor,appointment):
    subject = 'Confirmation of Appointment'
    message = f'Hi {patient.name}, Your appointment is confirmed for Dr. {doctor.name} {appointment.scheduled_time}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [patient.email, ]
    send_mail( subject, message, email_from, recipient_list )
    
def test_yourself(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in first')
        return redirect('login')
        
    return redirect('http://localhost:8501/')

# fetch the doctor appointments and confirm it 
def get_appointment(request, doctor_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in first')
        return redirect('login')

    today = timezone.now().date() + timezone.timedelta(days=1)
    end_date = today + timezone.timedelta(weeks=4)

    doctor = Doctor.objects.get(id=doctor_id)
    schedule = Schedule.objects.get(doctor=doctor)
    patient = Patient.objects.get(id=request.user.id)

    time_slots = []
    current_date = today
    while current_date <= end_date:
        current_datetime = datetime.combine(current_date, schedule.start_time)
        end_datetime = datetime.combine(current_date, schedule.end_time)

        while current_datetime <= end_datetime:
            time_slots.append(current_datetime)
            current_datetime += timedelta(hours=1)

        current_date += timedelta(days=1)

    existing_appointments = Appointment.objects.filter(doctor=doctor)
    available_time_slots = [time_slot for time_slot in time_slots if not existing_appointments.filter(scheduled_time=time_slot)]

    if request.method == 'POST':
        form = AppointmentForm(request.POST, available_time_slots=available_time_slots)
        if form.is_valid():
            selected_time = form.cleaned_data['scheduled_time']
            if selected_time:
                appointment = Appointment(patient=patient, doctor=doctor, scheduled_time=selected_time)
                appointment.save()
                send_email(patient,doctor,appointment)
                return redirect('get_homepage')
    else:
        form = AppointmentForm(available_time_slots=available_time_slots)

    return render(request, 'hospital/appointment.html', {'form': form, 'doctor': doctor, 'person': patient})

def fetch_appointments(request):
    patient = Patient.objects.get(User.objects.get(id=request.user_id).username)
    appointments = Appointment.objects.filter(patient_id=patient.id)
    print(appointments)

    return render(request, 'hospital/view_appointments.html', {'appointments' : appointments})

# successful login of the user 
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


# fetching the user information 
@login_required
def get_person(request):
    user = User.objects.get(id=request.user.id)
    person = Person.objects.get(email=user.username)
    is_doctor = person.is_doctor 


    if is_doctor:
        doctor = Doctor.objects.get(email=user.username)
        appointments = Appointment.objects.filter(doctor_id=doctor.id).order_by('scheduled_time')
    else:
        patient = Patient.objects.get(email=User.objects.get(id=request.user.id).username)
        appointments = Appointment.objects.filter(patient_id=patient.id).order_by('scheduled_time') 

    if request.method == 'POST':

        if is_doctor:
            form = DoctorForm(request.POST, instance=doctor)
        else:
            form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            # update user password in the User class too if the password gets changed 
            password = form.cleaned_data['password']
            user = User.objects.get(id=request.user.id)
            user.password = password

            form.save()
            print('Profile updated successfully')
            return redirect('get_homepage')
    else:
        if is_doctor:
            form = DoctorForm(instance=doctor)
        else:
            form = PatientForm(instance=patient)

    return render(request, 'hospital/person_details.html', {'form': form, 'appointments': appointments, 'is_doctor': is_doctor})

def logout_view(request):
    auth_logout(request)
    return redirect('get_homepage')

# views to implement forgot password
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password/custom_password_reset_email.html'
    success_url = reverse_lazy('custom_password_reset_done')
    subject_template_name = 'password/custom_password_reset_subject.txt'
    template_name = 'password/custom_password_reset_form.html'
    extra_email_context = {'person_model': Person}

    def form_valid(self, form):
        email = form.cleaned_data['email']
        person = Person.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(person.pk))
        token = default_token_generator.make_token(person)
        token_url = reverse_lazy('custom_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        # Construct reset URL
        reset_url = self.request.build_absolute_uri(token_url)

        # Pass reset_url as context to the email template
        context = {'reset_url': reset_url}

        # Update the email context with the context dictionary
        self.extra_email_context.update(context)

        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/custom_password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/custom_password_reset_confirm.html'
    success_url = reverse_lazy('login')