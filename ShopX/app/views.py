from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def Home(request):
    return  HttpResponse("Hello, this is a basic HTTP response.")

def Login(request):
    return HttpResponse("Login Page")