from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'censura/index.html')

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

def view_movies(request):
    return HttpResponse("Movies")

def view_movie(request):
    return HttpResponse("Movie")

def review(request):
    return HttpResponse("Movie review")

def create_review(request):
    return HttpResponse("Create Review")

