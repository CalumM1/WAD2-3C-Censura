from django.shortcuts import render
from django.http import HttpResponse
from censura.models import Movie

def index(request):
    return render(request, 'censura/index.html')

def login(request):
    return render(request, 'censura/login.html')

def my_account(request):
    return render(request, 'censura/account.html')

def my_favourites(request):
    return render(request, 'censura/favourites.html')

def my_reviews(request):
    return render(request, 'censura/read_review.html')

def signup(request):
    return render(request, 'censura/signup.html')

def about(request):
    return render(request, 'censura/about.html')

def view_movies(request):
    all_movies = Movie.objects.all()
    context_dict = {"movies" : all_movies}
    return render(request, 'censura/movies.html', context=context_dict)

def view_movie(request):
    return render(request, 'censura/movie.html')

def review(request):
    return render(request, 'censura/read_review.html')

def create_review(request):
    return render(request, 'censura/write_review.html')

