from django.urls import path
from . import views

urlpatterns = [
    path('add_person/', views.add_person, name='add_person'),
    path('success/', views.success, name='success'),
    path('login/', views.login, name='login'),
    path('person/<int:user_id>/', views.get_person, name='get_person'),
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('get_doctor/<str:keyword>/', views.get_doctor, name='get_doctor'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),


]
