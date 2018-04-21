from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from league.models import *


class SignUpForm(UserCreationForm):
    # summoner_name = forms.CharField(max_length=254, help_text='Required. Inform a valid summoner name.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Summoner
        fields = ('username', 'summoner_name', 'email', 'password1', 'password2',)
