from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Censura")

def login(request):
    return HttpResponse("Login Page")

def my_account(request):
    return HttpResponse("My Account")