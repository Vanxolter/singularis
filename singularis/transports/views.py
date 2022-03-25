from django.shortcuts import render
import logging
import folium
from geopy import Nominatim

from main import getroute
from main.models import RouteCoordinates

logger = logging.getLogger(__name__)


def walking():
    logger.info(f"walking")
    return ...


# Функция построения маршрута для машины
def auto(request, lat1, long1, lat2, long2, *args, **kwargs):
    name_from: list = [lat1, long1]
    name_to: list = [lat2, long2]
    geolocator = Nominatim(user_agent="my_request")
    location1 = geolocator.reverse(name_from)
    location2 = geolocator.reverse(name_to)
    coordinates = RouteCoordinates.objects.create(author=request.user, name_from=location1.address, name_to=location2.address,
                                                  startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
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


def trainhard():
    logger.info(f"train")
    return ...


def airplane(request, lat1, long1, lat2, long2, *args, **kwargs):
    name_from: list = [lat1, long1]
    name_to: list = [lat2, long2]
    geolocator = Nominatim(user_agent="my_request")
    location1 = geolocator.reverse(name_from)
    location2 = geolocator.reverse(name_to)
    coordinates = RouteCoordinates.objects.create(author=request.user, name_from=location1.address, name_to=location2.address,
                                                  startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
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