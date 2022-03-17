from django.contrib import admin

from .models import Airports


@admin.register(Airports)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name", "type", "latitude_deg", "longitude_deg")
    search_fields = ("name",)