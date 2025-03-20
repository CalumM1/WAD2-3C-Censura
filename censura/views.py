from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import UserForm, UserProfileForm, ReviewForm
from .models import UserProfile, Review

# from django.contrib.auth.models import User, UserProfile

from censura.models import Movie

from django.http import JsonResponse


def index(request):
    
    context_dict = {}
    
    movies_release_order = Movie.objects.order_by('-release_date')
    five_most_revent = movies_release_order[:5]
    context_dict['movies_release_order'] = five_most_revent
    
    return render(request, 'censura/index.html', context=context_dict)


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
    user_profile = get_object_or_404(UserProfile, user__username=username)
    user_reviews = Review.objects.filter(user=user_profile.user).order_by('-created_at')[:5]
    liked_movies = user_profile.likes.all()

    context = {
        'user_profile': user_profile,
        'user_reviews': user_reviews,
        'liked_movies': liked_movies,
    }
    return render(request, 'censura/account.html', context)

@login_required
def my_favourites(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    liked_movies = user_profile.likes.all().order_by('-release_date')

    paginator = Paginator(liked_movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'items': [
                {
                    'type': 'movie',
                    'name': movie.name,
                    'image': movie.image.url,
                    'director': movie.director,
                    'release_date': str(movie.release_date)
                } for movie in page_obj
            ],
            'has_next': page_obj.has_next(),
        })

    return render(request, 'censura/favourites.html', {'liked_movies': page_obj})
# def my_favourites(request):
#     return render(request, 'censura/favourites.html')


@login_required
def my_reviews(request, username):
    if request.user.username != username:
        return HttpResponseForbidden("You are not allowed to view this page.")

    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(user_reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'items': [
                {
                    'type': 'review',
                    'movie': review.movie.name,
                    'rating': review.rating,
                    'text': review.text
                } for review in page_obj
            ],
            'has_next': page_obj.has_next(),
        })

    return render(request, 'censura/read_review.html', {'reviews': page_obj})

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
            return redirect(reverse('censura:edit_profile', args=[user.username]))
    else:
        user_form = UserForm()

    return render(request, 'censura/signup.html', {'user_form': user_form})


@login_required
def edit_profile(request, username):
    user = request.user  
    if user.username != username:  # prevent others from editing
        return HttpResponseForbidden("You are not allowed to edit this profile.")

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user.userprofile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('censura:my_account', args=[user.username]))
    else:
        profile_form = UserProfileForm(instance=user.userprofile)

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

@login_required
def create_review(request, movie_name_slug=None):
    """
    Handles review creation. If accessed from a movie page, the movie is preselected.
    If accessed from 'My Account', the user can choose a movie.
    """
    movie = None

    # if provided a movie_name_slug, fetch the movie
    if movie_name_slug:
        movie = get_object_or_404(Movie, slug=movie_name_slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, movie_instance=movie)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # assign the current user
            if movie:
                review.movie = movie  # assign the movie if provided
            review.save()
            return redirect(reverse('censura:my_reviews', args=[request.user.username]))
    
    else:
        if movie:
            # if a movie was provided, remove movie selection from the form
            form = ReviewForm(movie_instance=movie)
        else:
            form = ReviewForm()

    return render(request, 'censura/write_review.html', {'form': form, 'movie': movie})

def ajax_search_movies(request):
    query = request.GET.get('query', '')
    if query:
        movies = Movie.objects.filter(name__icontains=query)[:10]  # Limit results
        movie_list = [{'name': movie.name} for movie in movies]
        return JsonResponse({'movies': movie_list})
    return JsonResponse({'movies': []})
