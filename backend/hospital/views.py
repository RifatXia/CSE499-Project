from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class TestView(APIView):
    def get(self, request):
        print("Entered")
        return Response("Hello Zia", status=200)