from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.forms import LocationForm
from main.models import Location

import logging

logger = logging.getLogger(__name__)

"""
Функция для ввода стартовой точки, при работе открывает карту с последними данными из базы данных
Если база пустая и карте не откуда брать данные дл отображение - происходит exceptи создается дефолтная точка
код повторяется - ПОЧИСТИТЬ
"""
def start(request):
    if request.method == "POST":
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            coordinates = Location.objects.create(author=request.user, **form.cleaned_data)
            logger.info(f"{request.user} added a new coordinates - {coordinates} ")
            return redirect("home")
    else:
        form = LocationForm()

    coordinates = Location.objects.last()
    try:
        latkoef = float(coordinates.startlat) * 0.99805
        longkoef = float(coordinates.startlong) * 0.99956
        return render(request, "main/map.html",
                      {"coordinates": coordinates, "latkoef": latkoef, "longkoef": longkoef, "form": form})
    except AttributeError: # Срабатывает если база пустая и неоткуда доставать координаты
        coordinates = Location.objects.create(author=request.user, startlat=53.9039, startlong=27.5546)
        latkoef = float(coordinates.startlat) * 0.99805
        longkoef = float(coordinates.startlong) * 0.99956
        logger.info(f" Создаю новую точку ")
        return render(request, "main/map.html",
                      {"coordinates": coordinates, "latkoef": latkoef, "longkoef": longkoef, "form": form})