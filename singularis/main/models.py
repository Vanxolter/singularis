from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models

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
    kash: dict = models.JSONField(verbose_name="Кэш для построения маршрута в истории", null=True, blank=True)
    transport: str = models.CharField(max_length=40, verbose_name="Вид транспорта", null=True, blank=False)


class Places(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=400, help_text="Что вы ищете?", verbose_name="Поиск", null=True, blank=False)
    places_long: float = models.FloatField(verbose_name="Долгота места", null=True, blank=True)
    places_lat: float = models.FloatField(verbose_name="Широта места", null=True, blank=True)


class Countries(models.Model):
    code: str = models.CharField(verbose_name="countries code", max_length=400, null=True, blank=True)
    name: str = models.CharField(verbose_name="countries name", max_length=400, null=True, blank=True)
    continent: str = models.CharField(verbose_name="countries continent", max_length=400, null=True, blank=True)
    wikipedia_link: str = models.URLField(verbose_name="home_link", null=True, blank=True)
    keywords: str = models.CharField(verbose_name="elevation", max_length=400, null=True, blank=True)


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name