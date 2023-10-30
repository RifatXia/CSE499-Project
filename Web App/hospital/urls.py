from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from .views import * 

urlpatterns = [
    path('add_person/', views.add_person, name='add_person'),
    path('success/', views.success, name='success'),
    path('login_view/', views.login_view, name='login'),
    path('person/', views.get_person, name='get_person'),
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('get_doctor/<str:keyword>/', views.get_doctor, name='get_doctor'),
    path('make_appointment/<doctor_id>', views.make_appointment, name='make_appointment'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='custom_password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
]