import random

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
import logging

from django.views.generic import FormView
from registration.forms import RegistrationForm

from singularis import settings
from users.forms import RegisterForm, Authorization
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


'''def generate_code():
    random.seed()
    return str(random.randint(10000,99999))'''


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.set_password(form.cleaned_data["password"])
            try:
                user.save()
                login(request, user)
                return redirect("mainsearch")
            except IntegrityError:
                return render(request, "errors/account_busy.html")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def authorization(request):
    if "_signin" in request.POST:
        form = Authorization(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f"Пользователь {form.cleaned_data} авторизировался")
                    return redirect("main")
            else:
                return HttpResponse("Аккаунта не существует")
    elif "_reg" in request.POST:
        return redirect("/users/")
    else:
        form = Authorization()
        return render(request, "users/authorization.html", {"form": form})


def logout_view(request):
    logger.info(f"Пользователь {request.user} вышел из своего аккаунта")
    logout(request)
    return redirect("/")


# РЕГИСТРАЦИЯ С ПОДТВЕРЖДЕНИЕ ПОРОЛЯ ЧЕРЕЗ ПОЧТУ
'''def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["email"]
                email = form.cleaned_data["email"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                my_password = form.cleaned_data.get('password')
                code = generate_code()
                message = code
                user = authenticate(username=username, password=my_password, email=email, first_name=first_name, last_name=last_name)
                send_mail('код подтверждения', message,
                settings.EMAIL_HOST_USER,
                ['errors@mail.ru'],
                fail_silently=False)
                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else: #тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Unknown or disabled account')
                    return render(request, 'registration/register.html', {'form': form})

            else:
                return render(request, 'registration/register.html', {'form': form})
        else:
            return render(request, 'registration/register.html', {'form':
            RegistrationForm()})
    else:
        return redirect('/personalArea/')'''