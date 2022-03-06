from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
import logging
from users.forms import RegisterForm, Authorization
from django.contrib.auth.models import User
from singularis.mixins import (
    reCAPTCHAValidation,
)

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            logger.info(f"Пользователь {form.cleaned_data} зарегестрировался")
            user = User(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            pas1 = user.set_password(form.cleaned_data["password1"])
            pas2 = user.set_password(form.cleaned_data["password2"])
            if pas1 == pas2:
                user.save()
                login(request, user)
            return redirect("home")
        #Добавить ошибку "Пороли не совподают"
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def authorization(request):
    if "_signin" in request.POST:
        form = Authorization(request.POST)
        if form.is_valid():
            logger.info(f"Пользователь {form.cleaned_data} авторизировался")
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("home")
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