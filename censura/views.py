from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from .models import UserProfile

# from django.contrib.auth.models import User, UserProfile


def index(request):
    return render(request, 'censura/index.html')

def user_login(request):
    return render(request, 'censura/login.html')

def my_account(request):
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
            return redirect('censura:edit_profile')

    else:
        user_form = UserForm()

    return render(request, 'censura/signup.html', {'user_form': user_form})

# @login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('my_account')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'censura/edit-profile.html', {'user_form': user_form, 'profile_form': profile_form})

def about(request):
    return render(request, 'censura/about.html')

def view_movies(request):
    return render(request, 'censura/movies.html')

def view_movie(request):
    return render(request, 'censura/movie.html')

def review(request):
    return render(request, 'censura/read_review.html')

def create_review(request):
    return render(request, 'censura/write_review.html')

