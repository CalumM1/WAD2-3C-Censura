from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Review

from .models import Movie

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    likes = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
        required=False)
    
    class Meta:
        model = UserProfile
        fields = ('likes',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'text': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, movie_instance=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If a movie instance is provided, remove the 'movie' field
        if movie_instance:
            self.fields.pop('movie', None)
