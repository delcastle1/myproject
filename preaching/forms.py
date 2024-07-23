from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from .models import GospelSong, PreacherProfile, PreachingSession, CustomUser

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    USER_ROLES = [
        ('preacher', 'Preacher'),
        ('artist', 'Artist'),
        ('admin', 'Admin'),
    ]
    
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=USER_ROLES, label='Register as', widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GospelSongForm(forms.ModelForm):
    class Meta:
        model = GospelSong
        fields = ['title', 'media_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class PreachingSessionForm(forms.ModelForm):
    class Meta:
        model = PreachingSession
        fields = ['title', 'description', 'scheduled_date', 'session_time', 'is_live']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'session_time': forms.Select(attrs={'class': 'form-control'}),
            'is_live': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PreacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = PreacherProfile
        fields = ['name', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    is_preacher = forms.BooleanField(required=False, label='Register as Preacher')
    is_artist = forms.BooleanField(required=False, label='Register as Artist')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_preacher', 'is_artist', 'password1', 'password2']
