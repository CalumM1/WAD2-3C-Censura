from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Censura")

def login(request):
    return HttpResponse("Login Page")

def my_account(request):
    return HttpResponse("My Account")

def my_favourites(request):
    return HttpResponse("My Favourites")

def my_reviews(request):
    return HttpResponse("My Reviews")

def signup(request):
    return HttpResponse("Sign Up")

def about(request):
    return HttpResponse("About")