from django.urls import path
from censura import views

app_name = 'censura'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', views.login, name='login'),
    
    path('signup/', views.signup, name='signup'),
    
    path('about/', views.about, name='about'),
    
    path('movies/', views.view_movies, name='movies'),
    
    path('movies/<slug:movie_name_slug>/', views.view_movie, name='movie'),
    
    path('movies/<slug:movie_name_slug>/review/<slug:username_slug>/', views.review, name='review'),
    
    path('movies/<slug:movie_name_slug>/create-review/', views.create_review, name='create_review'),
    
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('<slug:username_slug>/', views.my_account, name='my_account'),
    
    path('<slug:username_slug>/my-favourites/', views.my_favourites, name='my_favourites'),
    
    path('<slug:username_slug>/my-reviews/', views.my_reviews, name='my_reviews'),
]
