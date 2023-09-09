from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.

def Home(request):
    return HttpResponse("Home Page ")


def Login(request):
    return HttpResponse("Login Page")


def Register(request):
    return HttpResponse("SignUp Page")