from django.contrib import admin

from .models import Places, Countries


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ("author", "name",)
    fields = ("name", "places_long", "places_lat")
    search_fields = ("author", "name")


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    fields = ("code", "name")
    search_fields = ("code", "name")
