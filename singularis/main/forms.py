
from django import forms

from main.models import Places, RouteCoordinates


class SearchPlacesForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = ["name"]


class SearchRouteForm(forms.ModelForm):
    class Meta:
        model = RouteCoordinates
        fields = ["name_from", "name_to"]
