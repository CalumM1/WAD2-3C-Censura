from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    
class Movie(models.Model):
    pass

class Genre(models.Model):
    pass

class Comment(models.Model):
    pass

class Review(models.Model):
    pass
