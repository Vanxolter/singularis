
from django import forms

from main.models import Places


class SearchPlacesForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = ["places_long", "places_lat"]