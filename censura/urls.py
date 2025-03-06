from django.urls import path
from censura import views

app_name = 'censura'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('username/', views.my_account, name='my_account'),
    path('username/my-favourites/', views.my_favourites, name='my_favourites'),
    path('username/my-reviews/', views.my_reviews, name='my_reviews' ),
]
