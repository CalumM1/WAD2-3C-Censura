from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField('Movie', related_name='liked_by') 
    def __str__(self):
        return self.user.username


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Movie(models.Model):
    NAME_MAX_LENGTH = 50
    DESC_MAX_LENGTH = 500

    movie_id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField()
    description = models.TextField(max_length=DESC_MAX_LENGTH)
    director = models.CharField(
        max_length=NAME_MAX_LENGTH, default=None, blank=True, null=True)
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='movie_images/')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    pass
