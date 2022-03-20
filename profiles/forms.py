from django import forms

from .models import (
  Profile
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
  class Meta:
    model = User
    fields = ['username', 'password']

class ProfileModelForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = [
        'f_name',
        'l_name'
    ]

    labels = {
      'f_name': 'First name',
      'l_name': 'Last name'
    }