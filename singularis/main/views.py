from django.http import HttpResponse
from django.shortcuts import render, redirect
import folium
from main import getroute
from main.forms import SearchPlacesForm
from main.models import RouteCoordinates, Places

import logging

logger = logging.getLogger(__name__)


def showmap(request):
    """
    Функция для поиска месста на карте. При работе открывает карту с последними данными из базы Places
    Если база пустая и карте не откуда брать данные для отображение - создаем дефолтное значение
    """
    if request.method == "POST":
        form = SearchPlacesForm(request.POST, request.FILES)
        if form.is_valid():
            coordinates = Places.objects.create(author=request.user, **form.cleaned_data)
            logger.info(f"{request.user} added a new coordinates - {coordinates.places_long}/{coordinates.places_lat} ")
            return redirect("home")
    else:
        form = SearchPlacesForm()
    if request.user.is_authenticated:
        """  Если пользователь авторизирован - при заходе на сайт грузится карта с его последним поиском  """
        coordinates = Places.objects.filter(author=request.user).last()
        if coordinates:
            """  Если в базе есть координаты - отображаем последние введенные  """
            logger.info(f"{request.user} search place by coordinates - {coordinates.places_long} / {coordinates.places_lat} ")
            return render(request,'main/showmap.html', {"form": form, "coordinates": coordinates})
        else:
            """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
            coordinates = Places.objects.create(author=request.user, places_long=53.9018, places_lat=27.5610)
            logger.info(f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")
            return render(request,'main/showmap.html', {"form": form, "coordinates": coordinates})
    else:
        """  Если пользователь НЕ авторизован выводим на экран координаты с первой строки базы (по дефолту всегда Минск)  """
        coordinates = Places.objects.first()
        if coordinates:
            logger.info(
                f"{request.user} sees defoult place - {coordinates.places_long} / {coordinates.places_lat} ")
            return render(request, 'main/showmap.html', {"form": form, "coordinates": coordinates})
        else:
            """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
            coordinates = Places.objects.create(author_id=1, places_long=53.9018, places_lat=27.5610)
            logger.info(
                f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")
            return render(request, 'main/showmap.html', {"form": form, "coordinates": coordinates})


def showroute(request,lat1,long1,lat2,long2):
    coordinates = RouteCoordinates.objects.create(author=request.user, startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
    logger.info(f"{request.user} search route with coordinates - {coordinates} ")
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


def my_routes(request):
    routes = RouteCoordinates.objects.filter(author=request.user)

    return render(request,"main/places.html", {"route": routes},)