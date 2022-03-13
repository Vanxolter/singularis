
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': "*Ваше имя.."}))
    last_name = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput(attrs={'placeholder': "*Ваша фамилия.."}))
    email = forms.EmailField(max_length=254, required=True,
                                widget=forms.TextInput(attrs={'placeholder': "*Ваш email.."}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "*Пароль..", "class": "password"}))


class Authorization(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())

