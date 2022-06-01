from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
import logging

from django.views.generic import FormView

from singularis import settings
from users.forms import RegisterForm, Authorization
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


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
            user.save()
            logger.info(f"Пользователь {form.cleaned_data} зарегестрировался")
            login(request, user)
            return redirect("mainsearch")
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


