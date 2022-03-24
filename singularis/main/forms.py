
from django import forms
from django.core.exceptions import ValidationError
from main.models import Places, RouteCoordinates
from .models import ORDER_BY_TRANSPORTS


class SearchPlacesForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = ["name"]


class SearchRouteForm(forms.ModelForm):
    class Meta:
        model = RouteCoordinates
        fields = ["name_from", "name_to"]


class TransportsForm(forms.Form):
    feet = forms.BooleanField(required=False)
    autobus = forms.BooleanField(required=False)
    train = forms.BooleanField(required=False)
    fly = forms.BooleanField(required=False)