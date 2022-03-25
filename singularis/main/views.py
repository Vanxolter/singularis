from django.shortcuts import render, redirect
from main.models import RouteCoordinates, Places
from geopy.geocoders import Nominatim
import logging

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
    transport_list = ['feet', 'autobus', 'train', 'fly']
    if request.method == "POST":
        place_form = SearchPlacesForm(request.POST)
        route_form = SearchRouteForm(request.POST)
        transport_form = TransportsForm(request.POST)
        if place_form.is_valid(): # Форма поиска мест
            name: str = place_form.cleaned_data["name"]
            geolocator = Nominatim(user_agent="my_request") # Обращаюсь к библиотечке для геокодирования, а как она работает не е*у (Инкапсуляция) ¯\_(ツ)_/¯
            location = geolocator.geocode(name) # Геокодирую по назвнию точки
            logger.info(f"{request.user} added location - {location.address} ")
            coordinates = Places.objects.create(author=request.user, name=location.address, places_long=location.latitude,
                                                places_lat=location.longitude) # Обновляю данные в базе (добовляю координаты)  для нашего места
            return redirect("home")

        elif route_form.is_valid() and transport_form.is_valid(): # Форма прокладки маршрута
            name_from: str = route_form.cleaned_data["name_from"]
            name_to: str = route_form.cleaned_data["name_to"]
            geolocator = Nominatim(user_agent="my_request")
            location1 = geolocator.geocode(name_from)
            location2 = geolocator.geocode(name_to)

            feet: bool = transport_form.cleaned_data["feet"]
            automable: bool = transport_form.cleaned_data["auto"]
            train: bool = transport_form.cleaned_data["train"]
            fly: bool = transport_form.cleaned_data["fly"]

            my_choise: dict= {"feet": feet, "auto": automable, "train": train, "fly": fly}
            logger.info(f"check my choise - {my_choise}, {type(my_choise)} ")

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
                logger.info(
                    f"{request.user} search place by coordinates - {coordinates.places_long} / {coordinates.places_lat} ")
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
            else:
                """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
                coordinates = Places.objects.create(author=request.user, name="Минск, Беларусь", places_long=53.9018, places_lat=27.5610)
                logger.info(
                    f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
        except TypeError:
            coordinates = Places.objects.first()
            if coordinates:
                logger.info(
                    f"{request.user} sees defoult place - {coordinates.places_long} / {coordinates.places_lat} ")
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})
            else:
                """  Если в базе нет координат - создаем дефолтное значение (Минск)  """
                coordinates = Places.objects.create(author_id=13, name="Минск, Беларусь", places_long=53.9018, places_lat=27.5610)
                logger.info(
                    f"Database is empty, create defoult values - {coordinates.places_long} / {coordinates.places_lat} ")
                return render(request, 'main/showmap.html', {"place_form": place_form, "coordinates": coordinates, "route_form": route_form, "transport_form": transport_form})



'''def my_test(request):
    transport_list = ['feet', 'autobus', 'train', 'fly']
    if request.method == "POST":
        transports = request.POST.getlist('transports')
        print(transports)
        if transports == ['feet']:
            print("You selected feet")
        elif transports == ['autobus']:
            print("You selected autobus")
        elif transports == ['train']:
            print("You selected train")
        elif transports == ['fly']:
            print("You selected fly")
    return render(request, "test/checkbox.html")'''


'''class MainView(TemplateView):
    template_name = 'main/showmap.html'

    def get(self, request, *args, **kwargs):
        place_form = SearchPlacesForm(request.POST)
        route_form = SearchRouteForm(request.POST)
        context = self.get_context_data(**kwargs)
        context['place_form'] = place_form
        context['route_form'] = route_form
        return self.render_to_response(context)


class SearchPlacesFormView(FormView):
    form_class = SearchPlacesForm
    template_name = 'main/showmap.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        place_form = self.form_class(request.POST)
        route_form = SearchRouteForm()
        if place_form.is_valid():
            name = place_form.cleaned_data["name"]
            geolocator = Nominatim(
                user_agent="my_request")  # Обращаюсь к библиотечке для геокодирования, а как она работает не е*у (Инкапсуляция) ¯\_(ツ)_/¯
            location = geolocator.geocode(name)  # Геокодирую по назвнию точки
            logger.info(f"{request.user} added location - {location.address} ")
            coordinates = Places.objects.create(author=request.user, name=location.address,
                                                places_long=location.latitude,
                                                places_lat=location.longitude)  # Обновляю данные в базе (добовляю координаты)  для нашего места
            return self.render_to_response(
                self.get_context_data(
                    success=True
                )
            )
        else:
            return self.render_to_response(
                self.get_context_data(
                    place_form=place_form,
                    route_form=route_form
                )
            )


class SearchRouteFormView(FormView):
    form_class = SearchRouteForm
    template_name = 'main/showmap.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        route_form = self.form_class(request.POST)
        place_form = SearchPlacesForm()
        if route_form.is_valid():
            name_from = route_form.cleaned_data["name_from"]
            name_to = route_form.cleaned_data["name_to"]
            geolocator = Nominatim(user_agent="my_request")
            location1 = geolocator.geocode(name_from)
            location2 = geolocator.geocode(name_to)
            return showroute(request, location1.latitude, location1.longitude, location2.latitude, location2.longitude)
        else:
            return self.render_to_response(
                self.get_context_data(
                    place_form=place_form,
                    route_form=route_form
                )
            )'''