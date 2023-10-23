from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name= 'get_homepage'),
    path('logout', views.logout_view),
]