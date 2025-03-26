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
    likes = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
        required=False)
    
    class Meta:
        model = UserProfile
        fields = ('likes', 'picture')


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
        
