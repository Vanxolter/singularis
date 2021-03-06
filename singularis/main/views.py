from datetime import datetime, date

from django.shortcuts import render, redirect
from main.models import RouteCoordinates, Places, News, Countries
from geopy.geocoders import Nominatim
import logging
from django.core.paginator import Paginator
import requests

# Forms
from main.forms import SearchPlacesForm, SearchRouteForm
from transports.forms import TransportsForm


# Types of transport
from transports.views import auto, walking, trainhard, airplane

logger = logging.getLogger(__name__)


def showmap(request):
    """
    Функция для поиска месста на карте. При работе открывает карту с последними данными из базы Places
    Если база пустая и карте не откуда брать данные для отображение - создаем дефолтное значение
    """
    if request.method == "POST":
        place_form = SearchPlacesForm(request.POST)
        route_form = SearchRouteForm(request.POST)
        transport_form = TransportsForm(request.POST)
        if place_form.is_valid(): # Форма поиска мест
            name: str = place_form.cleaned_data["name"]
            geolocator = Nominatim(user_agent="my_request") # Обращаюсь к библиотечке для геокодирования, а как она работает не е*у (Инкапсуляция) ¯\_(ツ)_/¯
            location = geolocator.geocode(name) # Геокодирую по назвнию точки
            try:
                coordinates = Places.objects.create(author=request.user, name=location.address, places_long=location.latitude,
                                                    places_lat=location.longitude) # Обновляю данные в базе (добовляю координаты)  для нашего места
                return redirect("mainsearch")
            except AttributeError:
                return redirect("mainsearch")

        elif route_form.is_valid() and transport_form.is_valid(): # Форма прокладки маршрута
            name_from: str = route_form.cleaned_data["name_from"]
            name_to: str = route_form.cleaned_data["name_to"]
            geolocator = Nominatim(user_agent="my_request")
            location1 = geolocator.geocode(name_from, language="en")
            location2 = geolocator.geocode(name_to, language="en")
            logger.info(f"___Solution22222 - {location1, location2} ")

            # Проверка инпута, если было введено название страны, то выстравиваем маршрут в столицу!
            def country_check(location1, location2):
                name_from = geolocator.reverse([location1.latitude, location1.longitude], language='en')
                sepa_from = name_from[-2].split(', ') # Достаю полное название страны из геокодирования
                '''variant = Countries.objects.get(name=sepa_from[-1]) # Достаю варианты названия страны из БД
                countrys_keywords = variant.keywords.split(', ') # Преобразую варианты в список'''
                logger.info(f"___введенные ДАННЫЕ - {location1} == {sepa_from[-1]} ")
                if str(location1) == sepa_from[-1]:
                    flag = True

                    url = "https://countriesnow.space/api/v0.1/countries/capital"
                    payload = {"country": f"{str(location1)}"}
                    headers = {}
                    response = requests.request("POST", url, headers=headers, data=payload)
                    res = response.json()
                    cap = [res['data']['capital']]
                    logger.info(f"___CAPITAL1 - {cap[0]} ")
                    location1 = geolocator.geocode(cap[0], language="en") # Координаты столица государства

                else:
                    flag = False
                    location1 = location1
                logger.info(f"___FLAAAAG - {flag} ")

                name_to = geolocator.reverse([location2.latitude, location2.longitude], language='en')
                sepa_to = name_to[-2].split(', ') # Достаю полное название страны из геокодирования
                '''variant = Countries.objects.get(name=sepa_from[-1]) # Достаю варианты названия страны из БД
                countrys_keywords = variant.keywords.split(', ') # Преобразую варианты в список'''
                logger.info(f"___введенные ДАННЫЕ - {location2} == {sepa_to[-1]} ")
                if str(location2) == sepa_to[-1]:
                    flag = True

                    url = "https://countriesnow.space/api/v0.1/countries/capital"
                    payload = {"country": f"{str(location2)}"}
                    headers = {}
                    response = requests.request("POST", url, headers=headers, data=payload)
                    res = response.json()
                    cap = [res['data']['capital']]
                    logger.info(f"___CAPITAL2 - {cap[0]} ")
                    location2 = geolocator.geocode(cap[0], language="en") # Координаты столица государства

                else:
                    flag = False
                    location2 = location2
                logger.info(f"___FLAAAAG - {flag} ")

                return location1, location2

            solution = country_check(location1, location2)
            location1 = solution[0]
            location2 = solution[1]
            logger.info(f"___Solution - {location1, location2} ")


            feet: bool = transport_form.cleaned_data["feet"]
            automable: bool = transport_form.cleaned_data["auto"]
            train: bool = transport_form.cleaned_data["train"]
            fly: bool = transport_form.cleaned_data["fly"]

            my_choise: dict= {"feet": feet, "auto": automable, "train": train, "fly": fly}

            if my_choise["feet"]:
                return walking()
            elif my_choise["auto"]:
                return auto(request, location1.latitude, location1.longitude, location2.latitude, location2.longitude)
            elif my_choise["train"]:
                return trainhard()
            elif my_choise["fly"]:
                return airplane(request, location1.latitude, location1.longitude, location2.latitude, location2.longitude)

    else:
        place_form = SearchPlacesForm()
        route_form = SearchRouteForm()
        transport_form = TransportsForm()
        """БЛОК НИЖЕ ОТВЕЧАЕТ ЗА ОТОБРАЖЕНИЕ КАРТЫ ПРИ ПЕРВОМ ЗАХОДЕ НА САЙТ"""
        try:
            coordinates = Places.objects.filter(author=request.user).last()
            if coordinates:
                """  Если в базе есть координаты - отображаем последние введенные  """
                '''logger.info(
                    f"{request.user} search place by coordinates - {coordinates.places_long} / {coordinates.places_lat} ")'''
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
            else:
                """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
                coordinates = Places.objects.create(author=request.user, name="Минск, Беларусь", places_long=53.9018, places_lat=27.5610)
                '''logger.info(
                    f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")'''
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
        except TypeError:
            coordinates = Places.objects.first()
            if coordinates:
                '''logger.info(
                    f"{request.user} sees defoult place - {coordinates.places_long} / {coordinates.places_lat} ")'''
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
            else:
                """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
                coordinates = Places.objects.create(author_id=13, name="Минск, Беларусь", places_long=53.9018, places_lat=27.5610)
                '''logger.info(
                    f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")'''
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})


def main(request):
    return render(request, 'main/main.html')


def analysis(request):
    return render(request, 'main/analysis.html')


def news(request):

    news = News.objects.all().order_by("id")

    paginator = Paginator(news, 30)
    page_number = request.GET.get("page")
    news = paginator.get_page(page_number)

    return render(
        request, 'news/news.html',
        {"news": news},
    )