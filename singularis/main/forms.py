
from django import forms

from main.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["startlong", "startlat", "endlong", "endlat"]