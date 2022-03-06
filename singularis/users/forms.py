
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': "*Ваше имя.."}))
    last_name = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput(attrs={'placeholder': "*Ваша фамилия.."}))
    email = forms.EmailField(max_length=254, required=True,
                                widget=forms.TextInput(attrs={'placeholder': "*Ваш email.."}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "*Пароль..", "class": "password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "*Повторите пароль..", "class": "password"}))

    # reCAPTHA token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)


class Authorization(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password', )