from django.contrib import admin

from .models import Places


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ("author", "name",)
    fields = ("name", "places_long", "places_lat")
    search_fields = ("author", "name")