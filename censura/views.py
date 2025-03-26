from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import UserForm, UserProfileForm, ReviewForm, CommentForm
from .models import UserProfile, Review, Movie, Comment
from django.http import JsonResponse


def index(request):

    context_dict = {}

    movies_release_order = Movie.objects.order_by('-release_date')
    five_most_revent = movies_release_order[:5]

    movies_by_popularity = Movie.objects.order_by('-popularity')
    five_most_popular = movies_by_popularity[:5]

    context_dict['movies_release_order'] = five_most_revent
    context_dict['movies_by_popularity'] = five_most_popular

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
    user_reviews = Review.objects.filter(
        user=user_profile.user).order_by('-created_at')[:5]
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

@login_required
def toggle_favourite(request, movie_name_slug):
    print("Toggle favourite view reached for:", movie_name_slug)
    movie = get_object_or_404(Movie, slug=movie_name_slug)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if movie in user_profile.likes.all():
        user_profile.likes.remove(movie)
        is_favourite = False
    else:
        user_profile.likes.add(movie)
        is_favourite = True

    return JsonResponse({'success': True, 'is_favourite': is_favourite})


@login_required
def my_reviews(request, username):
    if request.user.username != username:
        return HttpResponseForbidden("You are not allowed to view this page.")

    user_reviews = Review.objects.filter(
        user=request.user).order_by('-created_at')
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
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)

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
    context_dict = {"movies": movies}
    return render(request, 'censura/movies.html', context=context_dict)


def view_movie(request, movie_name_slug):
    context_dict = {}

    try:
        movie = Movie.objects.get(slug=movie_name_slug)
        movie.genre.prefetch_related("genre").all()
        context_dict['movie'] = movie

        if request.user.is_authenticated:
            user_has_reviewed = Review.objects.filter(
                movie=movie, user=request.user).exists()
            context_dict['user_has_reviewed'] = user_has_reviewed
            if user_has_reviewed:
                context_dict['user_reviews'] = Review.objects.filter(
                    movie=movie.movie_id, user_id=request.user.id)

        context_dict['all_reviews'] = Review.objects.filter(
            movie_id=movie.movie_id)

    except Movie.DoesNotExist:
        context_dict['movie'] = None

    context_dict['movie_name_slug'] = movie_name_slug

    return render(request, 'censura/movie.html', context=context_dict)


def review(request, movie_name_slug, username):
    
    movie = get_object_or_404(Movie, slug=movie_name_slug)
    user = UserProfile.objects.get(user__username=username).user
    review = get_object_or_404(Review, movie=movie, user=user)
    comments = Comment.objects.filter(review=review)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.review = review
            new_comment.save()
            
            return redirect(reverse('censura:review', args=[movie.slug, review.user.username]))
    else:
        form = CommentForm()

    context_dict = {
        'movie': movie,
        'review': review,
        'form': form,
        'comments': comments,
    }
    return render(request, 'censura/review_thread.html', context=context_dict)


@login_required
def create_review(request, movie_name_slug=None):
    movie = None
    review = None

    if movie_name_slug:
        movie = get_object_or_404(Movie, slug=movie_name_slug)
        try:
            review = Review.objects.get(user=request.user, movie=movie)
        except Review.DoesNotExist:
            pass

    if request.method == 'POST':
        if review:
            form = ReviewForm(request.POST, instance=review,
                              movie_instance=movie)
        else:
            form = ReviewForm(request.POST, movie_instance=movie)

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            if movie:
                new_review.movie = movie
            new_review.save()

            if movie:
                return redirect(reverse('censura:movie', args=[movie.slug]))
            else:
                return redirect(reverse('censura:my_reviews', args=[request.user.username]))

    else:
        if review:
            form = ReviewForm(instance=review, movie_instance=movie)
        elif movie:
            form = ReviewForm(movie_instance=movie)
        else:
            form = ReviewForm()

    context = {
        'form': form,
        'movie': movie,
        'edit_mode': review is not None
    }
    return render(request, 'censura/write_review.html', context)


def ajax_search_movies(request):
    query = request.GET.get('query', '')
    if query:
        movies = Movie.objects.filter(name__icontains=query)[
            :10]  # Limit results
        movie_list = [{'name': movie.name} for movie in movies]
        return JsonResponse({'movies': movie_list})
    return JsonResponse({'movies': []})


def ajax_sorted_reviews(request, movie_name_slug):
    movie = get_object_or_404(Movie, slug=movie_name_slug)
    sort_by = request.GET.get('sort', 'created_at')

    if sort_by == 'likes':
        reviews = Review.objects.filter(movie=movie).order_by('-likes')
    elif sort_by == 'rating':
        reviews = Review.objects.filter(movie=movie).order_by('-rating')
    else:
        reviews = Review.objects.filter(movie=movie).order_by('-created_at')

    reviews_data = [
        {
            "user": review.user.username,
            "rating": review.rating,
            "text": review.text,
            "likes": review.likes,
            "created_at": review.created_at.strftime("%B %d, %Y"),
        }
        for review in reviews
    ]

    return JsonResponse({'reviews': reviews_data})
