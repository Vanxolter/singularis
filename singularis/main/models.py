from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Location(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location")
    startlong: float = models.FloatField(verbose_name="Стартовая Долгота", null=True, blank=True)
    startlat: float = models.FloatField(verbose_name="Стартовая Широта", null=True, blank=True)

    '''endlong: float = models.FloatField(verbose_name="Конечная Долгота", null=True, blank=True)
    endlat: float = models.FloatField(verbose_name="Конечная Широта", null=True, blank=True)'''
