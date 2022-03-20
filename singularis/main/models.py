from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class RouteCoordinates(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    name_from: str = models.CharField(max_length=400, verbose_name="Откуда", null=True, blank=True)
    startlong: float = models.FloatField(verbose_name="Стартовая Долгота", null=True, blank=True)
    startlat: float = models.FloatField(verbose_name="Стартовая Широта", null=True, blank=True)
    name_to: str = models.CharField(max_length=400, verbose_name="Куда", null=True, blank=True)
    endlong: float = models.FloatField(verbose_name="Конечная Долгота", null=True, blank=True)
    endlat: float = models.FloatField(verbose_name="Конечная Широта", null=True, blank=True)


class Places(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=400, verbose_name="Поиск", null=True, blank=True)
    places_long: float = models.FloatField(verbose_name="Долгота места", null=True, blank=True)
    places_lat: float = models.FloatField(verbose_name="Широта места", null=True, blank=True)

