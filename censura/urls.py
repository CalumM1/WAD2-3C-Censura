from django.urls import path
from censura import views

app_name = 'censura'

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.user_login, name='login'),
    
    path('logout/', views.user_logout, name='logout'),

    path('signup/', views.signup, name='signup'),
    
    path('about/', views.about, name='about'),
    
    path('user/<str:username>/edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('user/<str:username>/create-review/', views.create_review, name='create_review_account'),

    path('user/<str:username>/', views.my_account, name='my_account'),

    path('user/<str:username>/my-favourites/', views.my_favourites, name='my_favourites'),

    path('user/<str:username>/my-reviews/', views.my_reviews, name='my_reviews'),
    
    path('user/<str:username>/add-friend/', views.add_friend, name='add_friend'),
    
    path('user/<str:username>/remove-friend/', views.remove_friend, name='remove_friend'),

    path('movies/', views.view_movies, name='movies'),

    path('movies/<slug:movie_name_slug>/toggle-favourite/', views.toggle_favourite, name='toggle_favourite'),
    
    path('movies/<slug:movie_name_slug>', views.view_movie, name='movie'),
    
    path('movies/<slug:movie_name_slug>/review/<str:username>', views.review, name='review'),
    
    path('movies/<slug:movie_name_slug>/create-review', views.create_review, name='create_review'),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),

    path('ajax/search-movies/', views.ajax_search_movies, name='ajax_search_movies'),
    
    path('movies/<slug:movie_name_slug>/sorted-reviews/', views.ajax_sorted_reviews, name='ajax_sorted_reviews'),

]
