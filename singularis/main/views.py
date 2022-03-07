from django.shortcuts import render, redirect
from main.forms import LocationForm
from main.models import Location

import logging

logger = logging.getLogger(__name__)


def main(request):
    if request.method == "POST":
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            coordinates = Location.objects.create(author=request.user, **form.cleaned_data)
            logger.info(f"{request.user} added a new coordinates - {coordinates} ")
            return redirect("home")
    else:
        form = LocationForm()
    coordinates = Location.objects.last()
    return render(request, "main/map.html", {"coordinates": coordinates, "form": form})