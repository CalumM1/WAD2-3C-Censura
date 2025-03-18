from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import UserForm, UserProfileForm
from .models import UserProfile

# from django.contrib.auth.models import User, UserProfile

from censura.models import Movie

from censura.models import Movie


def index(request):
    return render(request, 'censura/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('censura:my_account', args=[request.user.username]))
        else:
            return HttpResponse('invalid login details')
    return render(request, 'censura/login.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('censura:index'))

def my_account(request, username):
    return render(request, 'censura/account.html')

def my_favourites(request):
    return render(request, 'censura/favourites.html')

def my_reviews(request):
    return render(request, 'censura/read_review.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # hash password
            user.save()

            # create a UserProfile linked to this User
            UserProfile.objects.create(user=user)
            
            # Login the user
            login(request, user)
            return redirect(reverse('censura:edit_profile'))
    else:
        user_form = UserForm()

    return render(request, 'censura/signup.html', {'user_form': user_form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('censura:my_account', args=[request.user.username]))
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'censura/edit-profile.html', {'profile_form': profile_form})

def about(request):
    return render(request, 'censura/about.html')

def view_movies(request):
    all_movies = Movie.objects.all()
    paginator = Paginator(all_movies, 24)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    context_dict = {"movies" : movies}
    return render(request, 'censura/movies.html', context=context_dict)

def view_movie(request, movie_name_slug):
    context_dict = {}

    try:
        movie = Movie.objects.get(slug=movie_name_slug)
        movie.genre.prefetch_related("genre").all()
        context_dict['movie'] = movie

    except Movie.DoesNotExist:
        context_dict['movie'] = None

    return render(request, 'censura/movie.html', context=context_dict)

def review(request):
    return render(request, 'censura/read_review.html')

def create_review(request):
    return render(request, 'censura/write_review.html')

