from django.shortcuts import render, get_object_or_404, redirect
from main.models import Places, RouteCoordinates, Countries
from django.shortcuts import render
import logging
import folium
from urllib.error import HTTPError

logger = logging.getLogger(__name__)


def my_history(request):
    places = Places.objects.filter(author=request.user)
    routes = RouteCoordinates.objects.filter(author=request.user)
    return render(request, "main/history.html", {"places": places, "routes": routes},)


# УДАЛЕНИЕ МЕСТА
def delete_place(request, place_id):
    logger.info(f"My ident {place_id}")
    try:
        place = get_object_or_404(Places, id=place_id)
        place.delete()
    except:
        route = get_object_or_404(RouteCoordinates, id=place_id)
        route.delete()

    return redirect("history")


# ВИЗУАЛИЗАЦИЯ ИСТОРИИ МАРШРУТОВ
def jesus_eyes(request):
    query = RouteCoordinates.objects.filter(author=request.user, transport='airplane').all() # Достаю все маршруты с базы
    logger.info(f"My kash {query}")
    first = query.first()
    figure = folium.Figure()
    try:
        m = folium.Map(location=[(first.kash['start_point1'][0]), (first.kash['start_point1'][1])], zoom_start=10, )
        m.add_to(figure)
        num = 0
    except AttributeError:
        return redirect("history")
    for i in query: # Отрисовываю все маршруты по порядку (алгоритм имеет сложность O(n))
        route = i.kash
        logger.info(f"My route {i.name_to}")
        num += 1

        folium.PolyLine(route['route1'], weight=8, color='orange', opacity=0.6, tooltip='Машиной', ).add_to(m)
        folium.Marker(location=route['start_point1'],icon=folium.Icon(icon='play', color='green')).add_to(m)
        folium.Marker(location=route['end_point1'],icon=folium.Icon(icon="cloud")).add_to(m)

        folium.PolyLine([route['end_point1'], route['start_point3']], weight=8, color='green', opacity=0.6,
                        tooltip=f'{num} Маршрут', ).add_to(m)

        folium.PolyLine(route['route3'], weight=8, color='orange', opacity=0.6, tooltip='Машиной', ).add_to(m)
        folium.Marker(location=route['start_point3'],icon=folium.Icon(icon="cloud")).add_to(m)
        folium.Marker(location=route['end_point3'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map':figure}
    return render(request,'main/showroute.html',context)


# ВИЗУАЛИЗАЦИЯ ИСТОРИИ МАРШРУТОВ
def one_route(request, route_id):
    query = RouteCoordinates.objects.filter(author=request.user, id = route_id, transport='airplane').first() # Достаю Определенный маршрут с базы по ID
    logger.info(f"My kash {query}")
    figure = folium.Figure()
    try:
        m = folium.Map(location=[(query.kash['start_point1'][0]), (query.kash['start_point1'][1])], zoom_start=10, )
        m.add_to(figure)
        num = 0
    except AttributeError:
        return redirect("history")

    route = query.kash
    logger.info(f"My route {query.name_to}")
    num += 1

    folium.PolyLine(route['route1'], weight=8, color='orange', opacity=0.6, tooltip='Машиной', ).add_to(m)
    folium.Marker(location=route['start_point1'],icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point1'],icon=folium.Icon(icon="cloud")).add_to(m)

    folium.PolyLine([route['end_point1'], route['start_point3']], weight=8, color='green', opacity=0.6,
                    tooltip=f'{num} Маршрут', ).add_to(m)

    folium.PolyLine(route['route3'], weight=8, color='orange', opacity=0.6, tooltip='Машиной',).add_to(m)
    folium.Marker(location=route['start_point3'],icon=folium.Icon(icon="cloud")).add_to(m)
    folium.Marker(location=route['end_point3'],icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()
    context={'map': figure}
    return render(request,'main/showroute.html', context)