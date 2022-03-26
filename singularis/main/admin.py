from django.contrib import admin

from .models import Places, Countries, RouteCoordinates


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


@admin.register(RouteCoordinates)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("author", "name_from", "name_to")
    fields = ("author", "name_from", "name_to")
    search_fields = ("author",)
