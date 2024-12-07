
from django import forms

from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    """
    Form for creating new Advertisement
    """
    class Meta:
        """ Meta class for AdvertisementForm"""
        model = Advertisement
        fields = ['title', 'content', 'img']

class SignUpForm(UserCreationForm):
    """ Form for creating new user """
    class Meta:
        """ Meta class for SignUpForm """
        model = User
        fields = ('username', 'password1', 'password2',)

