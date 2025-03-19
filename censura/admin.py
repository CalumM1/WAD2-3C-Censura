from django.contrib import admin
from censura.models import Movie, Genre, UserProfile

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(UserProfile)
