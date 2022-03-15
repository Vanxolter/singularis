from django.http import HttpResponse
from django.shortcuts import render, redirect
import folium
from main import getroute
from main.forms import LocationForm
from main.models import StartLoc

import logging

logger = logging.getLogger(__name__)

"""
Функция для ввода стартовой точки, при работе открывает карту с последними данными из базы данных
Если база пустая и карте не откуда брать данные дл отображение - происходит exceptи создается дефолтная точка
код повторяется - ПОЧИСТИТЬ
"""

def showmap(request):
    if request.method == "POST":
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            coordinates = StartLoc.objects.create(author=request.user, **form.cleaned_data)
            logger.info(f"{request.user} added a new coordinates - {coordinates} ")
            return redirect("home")
    else:
        form = LocationForm()
    coordinates = StartLoc.objects.last()
    return render(request,'main/showmap.html', {"form": form, "coordinates": coordinates})


def showroute(request,lat1,long1,lat2,long2):
    logger.info(f"{lat1} / {long1} / {lat2} / {long2}")
    coordinates = StartLoc.objects.create(author=request.user, startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
    logger.info(f"{request.user} search route with this coordinates - {coordinates} ")
    figure = folium.Figure()
    lat1,long1,lat2,long2=float(lat1),float(long1),float(lat2),float(long2)
    route=getroute.get_route(long1,lat1,long2,lat2)
    m = folium.Map(location=[(route['start_point'][0]),
                                 (route['start_point'][1])],
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'],weight=8,color='blue',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'main/showroute.html',context)