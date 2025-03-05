from django.urls import path
from censura import views

app_name = 'censura'

urlpatterns = [
    path('', views.index, name='index'),
]
