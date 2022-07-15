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
import http.client

logger = logging.getLogger(__name__)

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "9cef4caf6cmsh10e822fccf92ed4p142d32jsndf25b4bb0113",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
    }

def walking(request, lat1, long1, lat2, long2, *args, **kwargs):
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
    route= getroute.get_route_walk(long1, lat1, long2, lat2)
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
    route= getroute.get_route_car(long1, lat1, long2, lat2)
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
    logger.info(f"[___ВХОДНЫЕ КООРДИНАТЫ: Пукт отправки -{lat1}, {long1}; Пункт назнаачения - {lat2}, {long2}]")

    # 1 СТАДИЯ Ищу ближайший аропорт от нашей точки отправки
    location1 = geolocator.reverse(name_from, language='en')
    country_1 = location1.address.split(", ")
    country_code_1 = Countries.objects.get(name=country_1[-1]) # Достаю из полного адреса название страны
    logger.info(f"___СТРАНА ОТПРАВКИ - {country_1[-1]} - {country_code_1.code} ")
    try:
        airport_from = Airports.objects.filter(iso_country=country_code_1.code, type='large_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long1) + Abs(F('latitude_deg') - lat1))).order_by('distance').first()
        logger.info(f"___КООРДИНАТЫ 1-ГО АЭРОПОРТА - {airport_from.longitude_deg}, {airport_from.latitude_deg}")
    except KeyError:
        airport_from = Airports.objects.filter(iso_country=country_code_1.code, type='medium_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long1) + Abs(F('latitude_deg') - lat1))).order_by('distance').first()
    air_lat_1 = airport_from.latitude_deg # Широта первого аэропорта
    air_long_1 = airport_from.longitude_deg # Долгота первого аэропорта
    air_icao_1 = airport_from.gps_code
    airportz_1 = geolocator.reverse([air_lat_1, air_long_1], language='ru')
    airport_1 = airportz_1.address.split(", ")
    num_1 = 1

    # Обращаюсь к API откуда достаю всю информацио об аэропортах по icao коду
    def airport_data(air_icao, num):
        conn.request("GET", f"/airports/icao/{air_icao}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        fin_data = data.decode("utf-8")
        logger.info(f"___ДАННЫЕ ПО {num} АЭРОПОРТУ: {fin_data}")

    solution = airport_data(air_icao_1, num_1) # Вызываю функцию с API

    logger.info(f"_______________________КОНТРОЛЬНАЯ ТОЧКА МЕЖДУ АЭРОПОРТАМИ_________________________________________")

    # 2 СТАДИЯ Ищу 2-рой аропорт близ точки прибытия
    location2 = geolocator.reverse(name_to, language='en')
    country_2 = location2.address.split(", ")
    country_code_2 = Countries.objects.get(name=country_2[-1]) # Достаю из полного адреса название страны
    logger.info(f"___СТРАНА ОТПРАВКИ - {country_2[-1]} - {country_code_2.code} ")
    try:
        airport_to = Airports.objects.filter(iso_country=country_code_2.code, type='large_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long2) + Abs(F('latitude_deg') - lat2))).order_by('distance').first()
        logger.info(f"___КООРДИНАТЫ 2-ГО АЭРОПОРТА - {type(airport_to.longitude_deg)}, {type(airport_to.latitude_deg)}")
    except KeyError:
        airport_to = Airports.objects.filter(iso_country=country_code_2.code, type='medium_airport').annotate(
            distance=Sqrt(Abs(F('longitude_deg') - long1) + Abs(F('latitude_deg') - lat1))).order_by('distance').first()
    air_lat_2 = airport_to.latitude_deg # Широта второго аэропорта
    air_long_2 = airport_to.longitude_deg # Долгота второго аэропорта
    air_icao_2 = airport_to.gps_code
    airportz_2 = geolocator.reverse([air_lat_2, air_long_2], language='ru')
    airport_2 = airportz_2.address.split(", ")
    num_2 = 2

    solution = airport_data(air_icao_2, num_2) # Вызываю функцию с API


    coordinates = RouteCoordinates.objects.create(author=request.user, name_from=location1.address, name_to=location2.address,
                                                  startlong=lat1, startlat=long1, endlong=lat2, endlat=long2)
    '''logger.info(f"{request.user} search route with coordinates - {coordinates} ")'''

    figure = folium.Figure()
    long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2 = float(long1),float(lat1), float(air_long_1), float(air_lat_1), float(air_long_2), float(air_lat_2), float(long2), float(lat2)
    route = getroute.get_route_fly(long1, lat1, air_long_1, air_lat_1, air_long_2, air_lat_2, long2, lat2)

    # ВНОШУ НАШ МАРШРУТ В ВИДЕ JSON-файла в базу для отображения истории
    update = RouteCoordinates.objects.filter(author=request.user, id=coordinates.id).update(kash=route, transport='airplane')
    try:
        m = folium.Map(location=[(route['start_point1'][0]), (route['start_point1'][1])], zoom_start=10, )
    except KeyError:
        return render(request, 'errors/Error.html')

    info = [route['steps1'], route['steps3']]

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