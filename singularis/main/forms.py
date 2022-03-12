
from django import forms

from main.models import StartLoc


class LocationForm(forms.ModelForm):
    class Meta:
        model = StartLoc
        fields = ["startlong", "startlat"]