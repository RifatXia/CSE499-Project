from django.urls import path
from . import views

urlpatterns = [
    path('add_person/', views.add_person, name='add_person'),
    path('success/', views.success, name='success'),
    path('login/', views.login, name='login'),
    path('person/<int:user_id>/', views.get_person, name='get_person'),
]
