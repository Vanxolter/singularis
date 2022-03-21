from django.shortcuts import render, get_object_or_404, redirect
from main.models import Places, RouteCoordinates
import logging

logger = logging.getLogger(__name__)


def my_history(request):
    places = Places.objects.filter(author=request.user)
    routes = RouteCoordinates.objects.filter(author=request.user)
    return render(request, "main/history.html", {"places": places, "routes": routes},)


# УДАЛЕНИЕ МЕСТА
def delete_place(request, place_id):
    place = get_object_or_404(Places, id=place_id)
    logger.info(f"Place with id = {place}, successfully deleted!")
    place.delete()
    return redirect("history")