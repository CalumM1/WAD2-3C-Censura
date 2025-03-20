from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

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
    popularity = models.FloatField()
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='movie_images/')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):

    movie = models.ForeignKey(
        'Movie', 
        on_delete=models.CASCADE, 
        related_name='reviews',
        # null=True,  
        # blank=True  
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        # null=True, 
        # blank=True
    )
    
    rating = models.IntegerField(default=0)
    text = models.TextField(default="No comment")
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        unique_together = ('user', 'movie')
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.name if self.movie else 'Unknown Movie'} ({self.rating}/10)"


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', 
        on_delete=models.CASCADE, 
        related_name='comments',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True,
        blank=True
    )
    text = models.TextField(default="No comment")  
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Unknown User'} on {self.review.movie.name if self.review else 'Unknown Movie'}"