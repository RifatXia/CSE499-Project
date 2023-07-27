from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class TestView(APIView):
    def get(self, request):
        data = {
            "name": "Zia",
            "age": "23"
        }
        return Response(data, status=200)
    
    def post(self, request):
        return Response("Hello Zia", status=200)