from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


ORDER_BY_TRANSPORTS = (
    ("feet", "Ногами"),
    ("autobus", "Автобусом"),
    ("train", "Поездом"),
    ("fly", "Небом"),
)


class RouteCoordinates(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="routs")
    name_from: str = models.CharField(max_length=400, verbose_name="Откуда", null=True, blank=False)
    startlong: float = models.FloatField(verbose_name="Стартовая Долгота", null=True, blank=True)
    startlat: float = models.FloatField(verbose_name="Стартовая Широта", null=True, blank=True)
    name_to: str = models.CharField(max_length=400, verbose_name="Куда", null=True, blank=False)
    endlong: float = models.FloatField(verbose_name="Конечная Долгота", null=True, blank=True)
    endlat: float = models.FloatField(verbose_name="Конечная Широта", null=True, blank=True)


class Places(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=400, verbose_name="Поиск", null=True, blank=False)
    places_long: float = models.FloatField(verbose_name="Долгота места", null=True, blank=True)
    places_lat: float = models.FloatField(verbose_name="Широта места", null=True, blank=True)


class Countries(models.Model):
    code: str = models.CharField(verbose_name="countries code", max_length=400, null=True, blank=True)
    name: str = models.CharField(verbose_name="countries name", max_length=400, null=True, blank=True)
    continent: str = models.CharField(verbose_name="countries continent", max_length=400, null=True, blank=True)
    wikipedia_link: str = models.URLField(verbose_name="home_link", null=True, blank=True)
    keywords: str = models.CharField(verbose_name="elevation", max_length=400, null=True, blank=True)