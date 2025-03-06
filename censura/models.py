from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Genre(models.Model):
    pass


class Movie(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    director = models.CharField(max_length=NAME_MAX_LENGTH)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to=MEDIA_ROOT)
    reviews = models.ManyToManyField()


class Comment(models.Model):
    pass


class Review(models.Model):
    pass
