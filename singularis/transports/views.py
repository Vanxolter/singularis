from django.shortcuts import render
import logging
import folium
from geopy import Nominatim
from transports.models import Airports
from transports import getroute
from main.models import RouteCoordinates, Countries

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
    route= getroute.get_route(long1, lat1, long2, lat2)
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

    # Ищу ближайший аропорт от нашей точки отправки
    location1 = geolocator.reverse(name_from, language='en')
    country_1 = location1.address.split(", ")
    country_code_1 = Countries.objects.get(name=country_1[-1]) # Достаю из полного адреса название страны
    airport_from = Airports.objects.filter(iso_country=country_code_1.code, type='large_airport').filter(latitude_deg__lte=(lat1+2), longitude_deg__lte=(long1+2), latitude_deg__gte=(lat1-2), longitude_deg__gte=(long1-2)).first()
    logger.info(f"Код страны отправки - {country_code_1.code}, Название аэропорта - {airport_from.name} ")
    air_lat_1 = airport_from.latitude_deg # Широта первого аэропорта
    air_long_1 = airport_from.longitude_deg # Долгота первого аэропорта

    location2 = geolocator.reverse(name_to, language='en')
    country_2 = location2.address.split(", ")
    country_code_2 = Countries.objects.get(name=country_2[-1]) # Достаю из полного адреса название страны
    airport_to = Airports.objects.filter(iso_country=country_code_2.code, type='large_airport').filter(latitude_deg__lte=(lat2+2), longitude_deg__lte=(long2+2), latitude_deg__gte=(lat2-2), longitude_deg__gte=(long2-2)).first()
    logger.info(f"Код страны прибытия - {country_code_2.code}, Название аэропорта - {airport_to.name} ")
    air_lat_2 = airport_to.latitude_deg # Широта второго аэропорта
    air_long_2 = airport_to.longitude_deg # Долгота второго аэропорта

    coordinates = RouteCoordinates.objects.create(author=request.user, name_from=location1.address, name_to=location2.address,
                                                  startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
    logger.info(f"{request.user} search route with coordinates - {coordinates} ")

    figure = folium.Figure()
    long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2 = float(long1),float(lat1), float(air_long_1), float(air_lat_1), float(air_long_2), float(air_lat_2), float(long2), float(lat2)
    route = getroute.get_route_fly(long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2)

    m = folium.Map(location=[(route['start_point'][0]), (route['start_point'][1])], zoom_start=10, )

    m.add_to(figure)
    folium.PolyLine(route['route'], weight=8, color='red', opacity=0.6, tooltip='Маршрут', ).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['airport_1'], icon=folium.Icon(icon="cloud")).add_to(m)
    folium.Marker(location=route['airport_2'], icon=folium.Icon(icon="cloud")).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'main/showroute.html',context)