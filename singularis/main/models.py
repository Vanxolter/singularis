from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Location(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    startlong: str = models.FloatField(verbose_name="Longitude", null=True, blank=True)
    startlat: str = models.FloatField(verbose_name="Latitude", null=True, blank=True)
    endlong: str = models.FloatField(verbose_name="Longitude", null=True, blank=True)
    endlat: str = models.FloatField(verbose_name="Latitude", null=True, blank=True)
