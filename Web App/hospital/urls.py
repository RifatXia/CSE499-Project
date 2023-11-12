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
    path('test_yourself/', views.test_yourself, name='test_yourself'),
    path('get_doctor/<str:keyword>/', views.get_doctor, name='get_doctor'),
    path('get_appointment/<doctor_id>', views.get_appointment, name='get_appointment'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='custom_password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
]