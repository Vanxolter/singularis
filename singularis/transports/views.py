from django.db.models.functions.math import Sqrt, Abs
from django.db.models import F
from django.shortcuts import render, redirect
import logging
import folium
from geopy import Nominatim
from transports.models import Airports
from transports import getroute
from main.models import RouteCoordinates, Countries
from main.models import WorldBorder
from django.contrib.gis.db.models.functions import Distance

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
    folium.PolyLine(route['route'],weight=8,color='orange',opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'main/showroute.html',context)


def trainhard():
    logger.info(f"train")
    return ...


# (v.2.0) ВТОРАЯ ВЕРСИЯ ПОСТРОЕНИЯ ВОЗДУШНОГО МАРШРУТА, ПОСТРОЕНИЕ ДОЛЬШЕ Т.К. ЗАДЕЙСТВУЕТ 3 ОТДЕЛЬНЫЕ ИТЕРАЦИИ ДЛЯ ПОТРОЕНИЯ МАРШРУТА
def airplane(request, lat1, long1, lat2, long2, *args, **kwargs):
    name_from: list = [lat1, long1]
    name_to: list = [lat2, long2]
    geolocator = Nominatim(user_agent="my_request")
    logger.info(f"ВХОДНЫЕ КООРДИНАТЫ - {lat1} - {long1} - {lat2} - {long2}")

    # Ищу ближайший аропорт от нашей точки отправки
    location1 = geolocator.reverse(name_from, language='en')
    country_1 = location1.address.split(", ")
    country_code_1 = Countries.objects.get(name=country_1[-1]) # Достаю из полного адреса название страны
    logger.info(f"СТРАНА - {country_1[-1]} - {country_code_1.code} ")
    try:
        airport_from = Airports.objects.filter(iso_country=country_code_1.code, type='large_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long1) + Abs(F('latitude_deg') - lat1))).order_by('distance').first()
        logger.info(f"1-Й АЭРОПОРТ - {airport_from.longitude_deg}, {airport_from.latitude_deg}")
    except KeyError:
        airport_from = Airports.objects.filter(iso_country=country_code_1.code, type='medium_airport').filter(
            latitude_deg__lte=(lat1 + 7), longitude_deg__lte=(long1 + 7),
            latitude_deg__gte=(lat1 - 7), longitude_deg__gte=(long1 - 7)).first()
        logger.info(f"ИЩУ ПО СРЕДНИМ АЭРОПОРТАМ")
    air_lat_1 = airport_from.latitude_deg # Широта первого аэропорта
    air_long_1 = airport_from.longitude_deg # Долгота первого аэропорта

    airportz_1 = geolocator.reverse([air_lat_1, air_long_1], language='ru')
    airport_1 = airportz_1.address.split(", ")

    logger.info(f"КОНТРОЛЬНАЯ ТОЧКА ")

    location2 = geolocator.reverse(name_to, language='en')
    country_2 = location2.address.split(", ")
    country_code_2 = Countries.objects.get(name=country_2[-1]) # Достаю из полного адреса название страны
    logger.info(f"СТРАНА - {country_2[-1]} - {country_code_2.code} ")
    try:
        airport_to = Airports.objects.filter(iso_country=country_code_2.code, type='large_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long2) + Abs(F('latitude_deg') - lat2))).order_by('distance').first()
        logger.info(f"1-Й ТИП - {type(airport_to.longitude_deg)}, {type(airport_to.latitude_deg)}")
    except KeyError:
        airport_to = Airports.objects.filter(iso_country=country_code_2.code, type='medium_airport').filter(
            latitude_deg__lte=(float(lat2) + 7), longitude_deg__lte=(float(long2) + 7),
            latitude_deg__gte=(float(lat2) - 7), longitude_deg__gte=(float(long2) - 7)).first()
        logger.info(f"ИЩУ ПО СРЕДНИМ АЭРОПОРТАМ")
    air_lat_2 = airport_to.latitude_deg # Широта второго аэропорта
    air_long_2 = airport_to.longitude_deg # Долгота второго аэропорта

    airportz_2 = geolocator.reverse([air_lat_2, air_long_2], language='ru')
    airport_2 = airportz_2.address.split(", ")

    #IATA
    iata = f"https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{airport_1[-3]}%20в%20{airport_2[-3]}"
    logger.info(f"КОНТРОЛЬНАЯ {iata} ")

    coordinates = RouteCoordinates.objects.create(author=request.user, name_from=location1.address, name_to=location2.address,
                                                  startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
    logger.info(f"{request.user} search route with coordinates - {coordinates} ")

    figure = folium.Figure()
    long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2 = float(long1),float(lat1), float(air_long_1), float(air_lat_1), float(air_long_2), float(air_lat_2), float(long2), float(lat2)
    route = getroute.get_route_fly(long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2)

    # ВНОШУ НАШ МАРШРУТ В ВИДЕ JSON-файла в базу для отображения истории
    update = RouteCoordinates.objects.filter(author=request.user, id=coordinates.id).update(kash=route, transport='airplane')
    try:
        m = folium.Map(location=[(route['start_point1'][0]), (route['start_point1'][1])], zoom_start=10, )
    except KeyError:
        return redirect("home")

    info = [route['steps1'], route['steps3']]
    logger.info(f"INFOOOOO {info} ")

    m.add_to(figure)
    folium.PolyLine(route['route1'], weight=8, color='orange', opacity=0.6, tooltip=route['distance1'], ).add_to(m)
    folium.Marker(location=route['start_point1'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point1'],icon=folium.Icon(icon="cloud")).add_to(m)

    folium.PolyLine([[air_lat_1, air_long_1], [air_lat_2, air_long_2]], weight=8, color='green', opacity=0.6, tooltip='Самолетом', ).add_to(m)

    folium.PolyLine(route['route3'], weight=8, color='orange', opacity=0.6, tooltip=route['distance3'], ).add_to(m)
    folium.Marker(location=route['start_point3'],icon=folium.Icon(icon="cloud")).add_to(m)
    folium.Marker(location=route['end_point3'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure, 'info': info}
    return render(request,'main/showroute.html',context)