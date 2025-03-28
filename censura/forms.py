from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Review, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        labels = {
            'username': 'Your Username',
            'email': 'Email Address',
            'password': 'Create Password',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('picture',)
    


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.movie_instance = kwargs.pop('movie_instance', None)
        super().__init__(*args, **kwargs)
        if self.movie_instance:
            self.fields['movie'].initial = self.movie_instance
            self.fields['movie'].widget = forms.HiddenInput()

    class Meta:
        model = Review
        fields = ['movie', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 0, 
                'max': 10, 
                'class': 'form-control rating-selector'
            }),
            'text': forms.Textarea(attrs={'rows': 3}),
        }
            
class CommentForm(forms.ModelForm):
    text = forms.TextInput()
    class Meta:
        model = Comment
        fields = ('text',)
        
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 3
            }),
        }
        labels = {
            'text': 'Leave a comment',
        }
        
