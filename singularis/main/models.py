from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class StartLoc(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    startlong: float = models.FloatField(verbose_name="Стартовая Долгота", null=True, blank=True)
    startlat: float = models.FloatField(verbose_name="Стартовая Широта", null=True, blank=True)
    endlong: float = models.FloatField(verbose_name="Конечная Долгота", null=True, blank=True)
    endlat: float = models.FloatField(verbose_name="Конечная Широта", null=True, blank=True)


'''Убрать ограничитель наполя поставитть TextField (Почистить и перезалить базу)'''
class Airports(models.Model):
    airid: int = models.CharField(verbose_name="airports id",max_length=400, null=True, blank=True)
    ident: str = models.CharField(verbose_name="ident code", max_length=400, null=True, blank=True)
    type: str = models.CharField(verbose_name="type by airports", max_length=400, null=True, blank=True)
    name: str = models.CharField(verbose_name="name airports", max_length=400, null=True, blank=True)
    latitude_deg: str = models.CharField(verbose_name="latitude", max_length=400, null=True, blank=True)
    longitude_deg: str = models.CharField(verbose_name="longitude", max_length=400, null=True, blank=True)
    elevation_ft: str = models.CharField(verbose_name="elevation", max_length=400, null=True, blank=True)
    continent: str = models.CharField(verbose_name="continent", max_length=400, null=True, blank=True)
    iso_country: str = models.CharField(verbose_name="iso_country", max_length=400, null=True, blank=True)
    iso_region: str = models.CharField(verbose_name="iso_region", max_length=400, null=True, blank=True)
    municipality: str = models.CharField(verbose_name="municipality", max_length=400, null=True, blank=True)
    scheduled_service: str = models.CharField(verbose_name="scheduled_service", max_length=400, null=True, blank=True)
    gps_code: str = models.CharField(verbose_name="gps_code", max_length=400, null=True, blank=True)
    iata_code: str = models.CharField(verbose_name="iata_code", max_length=400, null=True, blank=True)
    local_code: str = models.CharField(verbose_name="local_code", max_length=400, null=True, blank=True)
    home_link: str = models.URLField(verbose_name="home_link", null=True, blank=True)
    wikipedia_link: str = models.URLField(verbose_name="wikipedia_link", null=True, blank=True)
    keywords: str = models.CharField(verbose_name="keywords", max_length=400, null=True, blank=True)